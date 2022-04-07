import os

import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
#     search = db.execute("SELECT DISTINCT a.acronym AS symbol,c.company,SUM(ua.quantity) AS shq,c.price FROM users AS u INNER JOIN user_actions AS ua ON ua.id_users = u.id INNER JOIN actions AS a ON a.id_actions = ua.id_actions INNER JOIN codes AS c ON c.id_codes = a.code WHERE u.id = :user_id GROUP BY a.acronym;",user_id=session.get("user_id"))
#     select = db.execute("SELECT cash FROM users WHERE id = :user_id",user_id=session.get("user_id"))
#     money = 0
#     for item in search:
#         money += int(item['shq'])*float(item['price'])
    return render_template("listQuotesUser.html"),200


@app.route("/history")
@login_required
def history():
    search = db.execute("SELECT DISTINCT a.acronym,c.company,h.type,quantity,price FROM users AS u INNER JOIN history AS h ON h.id_history_user = u.id INNER JOIN actions AS a ON a.id_actions = h.id_history_acronym INNER JOIN codes AS c ON c.id_codes = a.code WHERE u.id = :id_user ORDER BY created_at DESC;",id_user=session.get("user_id"))
    return render_template("history.html",query=search),200


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        username = request.form.get("username")
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html"),200


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html"),200
    elif request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid symbol!", 400)

        return render_template("quoted.html", name=stock["name"], symbol=stock["symbol"], price=stock["price"])


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        if not request.form.get("password"):
            return apology("must provide password", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords are not identical",400)
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)
        cash = 0
        has_user = db.execute("SELECT username FROM users;")
        for x in has_user:
            if (request.form.get("username") == x['username']):
                return apology("Username Exists", 400)
        query = db.execute("INSERT INTO USERS (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=hashed_password)
        return render_template("login.html"),200

    elif request.method == "GET":
        return render_template("register.html"),200


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        query = db.execute("SELECT symbol FROM user_quotes WHERE id_user_quote = :id_user",id_user=session.get("user_id"))
        return render_template("sell.html",items=query),200
    elif request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid symbol!", 400)

        qnt = request.form.get("shares")
        if (re.search(r'\D',qnt)):
            return apology("Invalid shares!", 400)

        if(int(qnt)<=0):
            return apology("TODO",400)
        selling = stock["price"]*int(qnt)
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id",user_id=session.get("user_id"))

        how_many = db.execute("SELECT shares FROM user_quotes WHERE id_user_quote = :id_user AND symbol = :symbol",id_user=session.get("user_id"),symbol=request.form.get("symbol"))[0]['shares']
        if (int(qnt)>int(how_many)):
            return apology("TODO",400)
        update_money = db.execute("UPDATE users SET cash = :new_cash WHERE id = :id_user",new_cash=((cash[0]['cash'])+selling),id_user=session.get("user_id"))

        history = db.execute("INSERT INTO history(type,quantity,id_history_acronym,id_history_user) VALUES ('Sell',:quantity,:acronym,:user);",quantity=qnt,acronym=request.form.get("symbol"),user=session.get("user_id"))

        money_current = abs(db.execute("SELECT cash FROM users WHERE id = :user_id",user_id=session.get("user_id"))[0]['cash'])

        return render_template("selling.html",symbol=stock["name"], price=float(stock["price"]), value_of_holding=int(qnt) * float(stock["price"]), cash=money_current)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html"),200
    elif request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid symbol!", 400)

        qnt = request.form.get("shares")
        if (re.search(r'\D',qnt)):
            return apology("Invalid shares!", 400)

        cost = stock["price"]*int(qnt)

        cash = db.execute("SELECT cash FROM users WHERE id = :user_id",user_id=session.get("user_id"))

        update_money = db.execute("UPDATE users SET cash = :new_cash WHERE id = :id_user",new_cash=((cash[0]['cash'])-cost),id_user=session.get("user_id"))

        history = db.execute("INSERT INTO history(type,quantity,id_history_acronym,id_history_user) VALUES ('Buy',:quantity,:acronym,:user);",quantity=qnt,acronym=request.form.get("symbol"),user=session.get("user_id"))

        search = db.execute("SELECT DISTINCT symbol FROM user_quotes WHERE id_user_quote = :id_user AND symbol = :symbol",id_user=session.get("user_id"),symbol=request.form.get("symbol"))
        if (len(search)>0):
            sharesAtuais = db.execute("SELECT shares FROM user_quotes WHERE id_user_quote = :id_user AND symbol = :symbol;",id_user=session.get("user_id"),symbol=request.form.get("symbol"))[0]['shares']
            newValue = qnt+int(sharesAtuais)
            quote = db.execute("UPDATE user_quotes SET shares = :shares WHERE id_user_quote=:id_user AND symbol= :symbol;",shares=newValue,symbol=request.form.get("symbol"),id_user=session.get("user_id"))
        else:
            quote = db.execute("INSERT INTO user_quotes(symbol,shares,id_user_quote) VALUES(:symbol,:shares,:id_user);",symbol=request.form.get("symbol"),shares=qnt,id_user=session.get("user_id"))

        money_current = abs(db.execute("SELECT cash FROM users WHERE id = :user_id;",user_id=session.get("user_id"))[0]['cash'])
        return render_template("bought.html",symbol=stock["name"], price=float(stock["price"]), value_of_holding=int(qnt) * float(stock["price"]), cash=money_current)

# @app.route("/sellQuote", methods=["POST"])
# @login_required
# def sellQuote():
#     if request.method == "POST":
#         acr = request.form.get("acronym")
#         qnt = request.form.get("quantity")
#         search = db.execute("SELECT DISTINCT a.acronym,c.company,SUM(ua.quantity) AS sua,c.price FROM users AS u INNER JOIN user_actions AS ua ON ua.id_users = u.id INNER JOIN actions AS a ON a.acronym = :acr AND ua.id_actions = a.id_actions JOIN codes AS c ON c.id_codes = a.code WHERE u.id = :user_id;",acr=acr,user_id=session.get("user_id"))
#         if len(search) == 1:
#             acronym = db.execute("SELECT id_actions FROM actions WHERE acronym = :ac",ac=acr)
#             quantit = db.execute("SELECT DISTINCT SUM(quantity) AS quantity FROM user_actions AS ua WHERE ua.id_actions = :id_actions AND ua.id_users = :user_id",id_actions=acronym[0]['id_actions'],user_id=session.get("user_id"))[0]['quantity']
#             if (int(qnt)>quantit):
#                 return apology("Not enought Quotes", 404)
#             elif(int(qnt)==quantit):
#                 delete = db.execute("DELETE FROM user_actions WHERE id_actions = :id_actions AND id_users = :user_id",id_actions=acronym[0]['id_actions'],user_id=session.get("user_id"))
#                 history = db.execute("INSERT INTO history(type,quantity,id_history_acronym,id_history_user) VALUES ('Sell',:quantity,:acronym,:user);",quantity=qnt,acronym=acronym[0]["id_actions"],user=session.get("user_id"))

#                 atual_cash = db.execute("SELECT cash FROM users WHERE id = :id_user;",id_user=session.get("user_id"))
#                 atual_price = db.execute("SELECT DISTINCT c.price FROM users AS u INNER JOIN actions AS a ON a.id_actions = :id_actions INNER JOIN codes AS c ON c.id_codes = a.code GROUP BY a.acronym;",id_actions = acronym[0]["id_actions"])

#                 future_cash = float(atual_cash[0]['cash'])+int(qnt)*float(atual_price)

#                 update = db.execute("UPDATE users SET cash = :future_cash WHERE id = :user_id",future_cash=future_cash,user_id=session.get("user_id"))
#             elif(int(qnt)<quantit): # Menor que o que tem no banco
#                 newValue = quantit-int(qnt)
#                 update = db.execute("UPDATE user_actions SET quantity = :quantity WHERE id_users= :user_id AND id_actions = :id_actions",quantity=newValue,user_id=session.get("user_id"),id_actions=acronym[0]['id_actions'])
#                 history = db.execute("INSERT INTO history(type,quantity,id_history_acronym,id_history_user) VALUES ('Sell',:quantity,:acronym,:user);",quantity=qnt,acronym=acronym[0]["id_actions"],user=session.get("user_id"))

#                 atual_cash = db.execute("SELECT cash FROM users WHERE id = :id_user;",id_user=session.get("user_id"))
#                 atual_price = db.execute("SELECT DISTINCT c.price FROM users AS u INNER JOIN actions AS a ON a.id_actions = :id_actions INNER JOIN codes AS c ON c.id_codes = a.code GROUP BY a.acronym;",id_actions = acronym[0]["id_actions"])
#                 future_cash = float(atual_cash[0]['cash'])+(int(qnt)*float(atual_price[0]['price']))
#                 update_cash = db.execute("UPDATE users SET cash = :future_cash WHERE id = :user_id",future_cash=future_cash,user_id=session.get("user_id"))
#         return redirect("/")

