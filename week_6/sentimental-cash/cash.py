import cs50
import math
global money, moedas

def is_money_valid(money):
    try:
        parsed = float(money)
        return parsed > 0
    except:
        return False


def main():
    money = input("Change owed: ")
    while (not is_money_valid(money)):
        money = input("Change owed: ")

    money = float(money)
    if (money == 0):
        print("0")
        return


    moedas = 0
    if (money>=0.25):
        moedas += money // 0.25
        money = round((money % 0.25),4)
        print(money)
    if (money >=0.10):
        moedas += money // 0.1
        money = round((money % 0.1),4)
        print(money)
    if (money>=0.05):
        moedas += money // 0.05
        money = round((money % 0.05),4)
        print(money)
    while(money>0):
        moedas += 1
        money = money - 0.01
    moedas = int(moedas)
    print(moedas)



main()