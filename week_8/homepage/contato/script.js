const btn = document.querySelector("#send-msg");
const name = document.querySelector("#name-text");
btn.addEventListener("click", ()=>{
    alert("Thanks for the message "+name.value+" :)");
})