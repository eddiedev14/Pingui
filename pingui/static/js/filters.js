const filtros = document.querySelectorAll(".activities__filter");

filtros.forEach(btn => {
    btn.addEventListener("click", () => {
        const filtro = btn.dataset.filter;

        // Quita la clase active de todos y añade al clicado
        filtros.forEach(f => f.classList.remove('activities__filter--active'));
        btn.classList.add('activities__filter--active');

        document.querySelectorAll(".activities__course").forEach(div => {
            const materia = div.dataset.materia;

            if (filtro === "todos" || materia === filtro) {
                div.style.display = "block";
            } else {
                div.style.display = "none";
            }
        });
    });
});