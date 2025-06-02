//Reproducir audio del preloader
const preloader = document.querySelector(".preloader");
const pathImg = document.querySelector(".path");
const audio = document.querySelector("audio");
const modal = document.querySelector("#modal");
const modalTryBtn = document.querySelector(".modal__button--try");
const modalTriesBtn = document.querySelector(".modal__button--tries");
const closeModalBtn = document.querySelector(".modal__close")

//* Ambient Sound
const ambientSoundAudio = document.querySelector("#ambient_sound");
const ambientSound = {
    "path_1": ["lake", "frog", "rabbit", "bird", "house"],
    "path_2": ["lake", "white_fox", "reindeer", "flower", "house"],
    "path_3": ["lake", "dog", "fox", "flower", "house"] 
}

const materiaInicialID = document.body.dataset.materiainicial;
let materiaSeleccionadaId = document.querySelector('.topic__btn--active')?.dataset.id;
const activitiesContainer = document.querySelector(".activities__container");

let fondoIndex = 1; // Comienza en 1 (path_1.png)
const totalFondos = 3;

document.addEventListener("DOMContentLoaded", () => {
    if (materiaInicialID !== "None") {
        cargarActividades(materiaInicialID)
    }
})

//Funcion para poner sonido
function playAudio() {
    audio.play();
    document.removeEventListener('mousemove', playAudio);
    document.removeEventListener('touchstart', playAudio);
}

document.addEventListener('mousemove', playAudio);
document.addEventListener('touchstart', playAudio);

setTimeout(() => {
    // Agrega la clase 'hide' para iniciar la animación de desvanecimiento
    preloader.classList.add('hide');

    // Escucha cuándo termina la transición de opacidad
    preloader.addEventListener('transitionend', () => {
        // Una vez que la transición ha terminado, establece display: none
        preloader.style.display = 'none';
    }, { once: true }); // { once: true } asegura que el evento se dispare solo una vez

}, 4000);

//Funcion para abrir y cerrar modal
closeModalBtn.addEventListener("click", closeModal)

function openModal(data) { 
    modal.querySelector("img").src = `/static/assets/${data.thumbnail}`;
    modal.querySelector(".modal__title").textContent = data.nombre;
    modal.querySelector(".modal__description").textContent = data.descripcion;
    modal.querySelector(".modal__course").textContent = obtenerMateriaSeleccionada();
    modal.querySelector(".modal__topic").textContent = data.tematica;

    modal.querySelector(".modal__button--try").href = `/estudiantes/actividades/${data.id}/iniciar/`;
    modal.querySelector(".modal__button--tries").href = `/estudiantes/actividades/${data.id}/intentos/`;

    modal.classList.remove('fade-out');
    modal.classList.add('fade-in');
    modal.showModal()
}

// Obtener el nombre de la materia activa
const obtenerMateriaSeleccionada = () => {
    const activeBtn = document.querySelector(".topic__btn--active");
    return activeBtn ? activeBtn.textContent.trim() : "";
};

function closeModal() { 
    modal.classList.remove('fade-in');
    modal.classList.add('fade-out');

    setTimeout(() => {
        modal.close();
        modal.classList.remove('fade-out');
    }, 300);
}

//* FUNCIONES PARA ACTIVIDADES
const botonesMaterias = document.querySelectorAll(".topic__btn");

//Añadir eventos para cambiar de materias
botonesMaterias.forEach(btn => {
    btn.addEventListener("click", () => {
        botonesMaterias.forEach(b => b.classList.remove("topic__btn--active"));
        btn.classList.add("topic__btn--active");

        // Cambiar el fondo cíclicamente
        updatePath();

        materiaSeleccionadaId = btn.dataset.id;
        cargarActividades(materiaSeleccionadaId);
    });
});

//Funcion para cargar las actividades de una materia
async function cargarActividades(id, pagina = 1) {
    try {
      const response = await fetch(`/estudiantes/actividades/${id}/?pagina=${pagina}`);
      const data = await response.json();
      renderizarActividades(data.actividades);

      // Mostrar u ocultar botones de paginación
      btnNext.style.display = data.hay_mas ? "flex" : "none";
      btnPrev.style.display = pagina > 1 ? "flex" : "none";
    } catch (error) {
      Swal.fire({
            title: "¡Error!",
            text: `¡Ha ocurrido un error obteniendo las actividades de la materia!`,
            icon: "error"
        });
    }
}

 // Función para renderizar actividades
function renderizarActividades(actividades){
    activitiesContainer.innerHTML = ""; // Limpiar
    position = 0;

    actividades.forEach(actividad => {
        position++;
        const iconoClase = actividad.estado === "complete" ?  "ri-checkbox-circle-fill" : "ri-error-warning-fill";

        const div = document.createElement("div");
        div.className = "icon " + (actividad.estado === "complete" ? "icon--complete" : "icon--pending");
        div.dataset.position = position;
        div.innerHTML = `
        <button data-id="${actividad.id}" data-nombre="${actividad.nombre}" data-descripcion="${actividad.descripcion}"
                data-thumbnail="${actividad.thumbnail}" data-tematica="${actividad.tematica}">
            <i class="${iconoClase}"></i>
        </button>
        `;

        //Si no se ha completado se oculta el boton de Ver mis intentos
        if (actividad.estado !== "complete") {
            modalTriesBtn.style.display = "none";
            modalTryBtn.style.gridColumn = "span 2";
        }else{
            modalTriesBtn.style.display = "block";
            modalTryBtn.style.gridColumn = "1";
        }

        // Evento para abrir el modal al hacer clic en una actividad
        div.querySelector("button").addEventListener("click", (e) => {
            let btn = e.target;

            //Se verifica obtener correctamente el botón
            if (btn.nodeName === "I") {
                btn = btn.parentElement;
            }

            openModal(btn.dataset);
        });

        activitiesContainer.appendChild(div);
    });

    //Evento para reproducir sonidos del ambiente
    const icons = document.querySelectorAll(".icon");
    icons.forEach(icon => icon.addEventListener("mouseenter", () => playAmbientSound(icon.dataset.position)))
};

function playAmbientSound(position) {
    const audioFile = ambientSound[`path_${fondoIndex}`][position - 1];
    ambientSoundAudio.src = `/static/assets/audio/ambient/${audioFile}.mp3`;
    ambientSoundAudio.play();
}

//* PAGINACIÓN
let paginaActual = 1;
const porPagina = 5;

const btnNext = document.querySelector(".pagination__btn--next");
const btnPrev = document.querySelector(".pagination__btn--previous");

btnNext.addEventListener("click", () => {
    paginaActual++
    activitiesContainer.innerHTML = ""; // Limpiar
    updatePath()
    cargarActividades(materiaSeleccionadaId, paginaActual);
});

btnPrev.addEventListener("click", () => {
    if (paginaActual > 1) {
        paginaActual--;
        activitiesContainer.innerHTML = ""; // Limpiar
        updatePath();
        cargarActividades(materiaSeleccionadaId, paginaActual);
    }
});

function updatePath() {
    // Cambiar el fondo cíclicamente
    pathImg.classList.remove(`path__${fondoIndex}`);
    fondoIndex = (fondoIndex % totalFondos) + 1;
    pathImg.classList.add(`path__${fondoIndex}`);
}