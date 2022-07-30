async function getResponse(btn){
    let form = btn.closest("btn btn-primary btn-shadow")
    let url = btn.closest("form").action
    let dataForm = new FormData(form)
    response = await fetch(url, {
        method : "POST",
        body : dataForm
    })
    .then(
        res => res.json()
    )
    .then(data => {
        btn.style.backgroundColor = "green"
        btn.style.color = "white"
        btn.disabled = true
    })
    .catch(err => {
        btn.style.color = "red"
    })
}

let buttons = document.querySelectorAll("input")
buttons.forEach(element => {
    element.addEventListener("click", (e) => {
        e.preventDefault()
        getResponse(element)
    })
});