const tableBody = document.querySelector(".table tbody");

document.addEventListener("DOMContentLoaded", () => {
  const queryParams = new URLSearchParams(window.location.search);

  if (queryParams.has("message")) {
      let message = queryParams.get("message");
      message = decodeURIComponent(message);
      Swal.fire({
          title: "¡Felicitaciones!",
          text: message,
          icon: "success"
      });
  }
})

tableBody.addEventListener("click", (e) => {
    let target = e.target;
    if (target.nodeName === "I") target = target.parentElement

    if (target.classList.contains("actions__delete")) {
        const id = target.dataset.id;

        Swal.fire({
            title: "¿Estás seguro?",
            text: "¿Deseas eliminar el registro seleccionado?",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            cancelButtonText: "Cancelar",
            confirmButtonText: "Sí, Eliminarlo"
          }).then((result) => {
            if (result.isConfirmed) {
              window.location.href = `${deleteURL}${id}/`
            }
          });
    }
})