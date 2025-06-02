const form = document.querySelector("form");

//Error Handler
document.addEventListener("DOMContentLoaded", () => {
    const queryParams = new URLSearchParams(window.location.search);

    if (queryParams.has("message")) {
        const message = queryParams.get("message");
        const icon = queryParams.get("icon");
        showLoginError(decodeURIComponent(message), icon);
    }
})

form.addEventListener("submit", (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    const isEmpty = Object.values(data).some(field => field === "");
    if (isEmpty) {
        showLoginError("Todos los datos son obligatorios. Completalos para continuar");
        return;
    } 

    form.submit();
})

function showLoginError(message, icon = null) {
    Swal.fire({
        title: icon ? "¡Felicitaciones!" : "¡Error!",
        text: message,
        icon: icon ? icon : "error"
    });
}