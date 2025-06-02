const startBtn = document.querySelector(".instructions__button");
const instructionsContainer = document.querySelector(".instructions")
const quizContainer = document.querySelector(".quiz__container");
const gameSoundAudio = document.querySelector("#gameSound")

const url = window.location.href;
const segments = url.split("/").filter(Boolean); // elimina elementos vacíos
const id = segments[segments.length - 2];

let nextButtonHandler = null;

//* Result
const result = document.querySelector(".result");
const resultImg = result.querySelector("img");
const resultTitle = document.querySelector(".result__title")
const resultMessage = document.querySelector(".result__message");
const resultGrade = document.querySelector(".card__value--grade");
const resultCorrect = document.querySelector(".card__value--correct")
const resultIncorrect = document.querySelector(".card__value--incorrect")
const restartActivityBtn = document.querySelector(".result__button--restart")

let totalPreguntas = 0;
let preguntaActual = 1;
let valorPorPregunta = 0;
let preguntasIncorrectas = [];

const opciones = {
    "0": "A",
    "1": "B",
    "2": "C",
    "3": "D"
}

const resultContent = {
    aprobado: {
        img: `/static/assets/img/oso_exito.png`,
        title: "🎉 ¡Excelente trabajo!",
        text: "Has aprobado con un excelente resultado. Sigue confiando en ti y avanzando con esa energía, ¡vas por muy buen camino!"
    },
    reprobado: {
        img: `/static/assets/img/oso_fracaso.png`,
        title: "🙁 Necesitamos practicar un poco más",
        text: "Aunque esta vez no aprobaste, cada intento te acerca más al éxito. Confía en tu proceso, aprende de los errores y vuelve a intentarlo."
    }
}

const progressFill = document.querySelector(".progress__fill");
const progressText = document.querySelector(".progress__text");
const nextBtn = document.querySelector(".next__button");
const questionArea = document.querySelector(".question__area");

//Evento cuando se presiona al boton de comenzar
startBtn.addEventListener("click", async () => {
    instructionsContainer.classList.add("hide")
    setTimeout(() => {
        instructionsContainer.style.display = "none";
        quizContainer.style.display = "flex"
        setTimeout(() => {
            quizContainer.classList.remove("hide");
        }, 300);
    }, 1000);

    //Se obtiene el numero de preguntas de esa actividad
    const response = await fetch(`/estudiantes/actividades/${id}/getQuestionsCount/`);
    const data = await response.json();
    totalPreguntas = data.total_preguntas;
    valorPorPregunta = 5 / totalPreguntas; // Se supone que la nota máxima es 5

    // Cargar primera pregunta
    cargarPregunta(preguntaActual);
})

//Funcion para cargar la pregunta actual
async function cargarPregunta() {
    try {
        const response = await fetch(`/estudiantes/actividades/${id}/pregunta/${preguntaActual}/`);
        const data = await response.json();

        renderizarPregunta(data);
        actualizarBarraProgreso();
    } catch (error) {
        console.error("Error al cargar la pregunta", error);
    }
}

function renderizarPregunta(data){
    const contenedor = document.querySelector(".question__area");
    contenedor.innerHTML = "";

    // Imagen
    if (data.imagen) {
        const imageContainer = document.createElement("div");
        imageContainer.classList.add("question__image");
        const img = document.createElement("img");
        
        // Extraer solo el nombre base del archivo original (e.g., "vocal a.png")
        const imageArray = data.imagen.split("/");
        const carpeta = imageArray[2];
        const nombreBase = imageArray[3]

        // Armar nueva ruta con el ID
        const nuevaRuta = `/static/assets/activities/assets/${carpeta}/${nombreBase}`;

        img.src = nuevaRuta;
        img.alt = "Imagen de la pregunta";
        img.classList.add("pregunta__imagen");

        contenedor.appendChild(imageContainer)
        imageContainer.appendChild(img);
    }

    const questionContainer = document.createElement("div");
    questionContainer.classList.add("question__container");

    // Texto de la pregunta
    const titulo = document.createElement("h2");
    titulo.textContent = `Pregunta #${preguntaActual}: ${data.texto}`;
    questionContainer.appendChild(titulo);

    // Opciones
    const opcionesContainer = document.createElement("div");
    opcionesContainer.className = "opciones__container";
    let opcionesPregunta

    //Verificamos si el tipo es seleccion_multiple o verdadero_falso
    if (data.tipo === "seleccion_multiple") {
        opcionesPregunta = data.opciones.split(",")
    }else{
        opcionesPregunta = ["Verdadero", "Falso"]
    }
    
    let respuestaSeleccionada = "";

    opcionesPregunta.forEach((opcion, index) => {
        const tile = document.createElement('div');
        tile.classList.add('radio-tile');

        if (data.tipo === "verdadero_falso") {
            const icon = document.createElement("img")
            icon.src = opcion === "Verdadero" ? "/static/assets/img/check.png" : "/static/assets/img/cross.png";
            tile.appendChild(icon)
        }

        const label = document.createElement('div');
        label.classList.add('radio-label');
        label.textContent = opcion;

        if (data.tipo === "seleccion_multiple") {
            label.dataset.answer = opciones[index];
        }

        tile.appendChild(label);
        opcionesContainer.appendChild(tile);

        tile.addEventListener('click', () => {
            // Quitar selección de todos
            document.querySelectorAll('.radio-tile').forEach(t => t.classList.remove('selected'));
            // Seleccionar este
            tile.classList.add('selected');
            // Guardar la respuesta seleccionada
            respuestaSeleccionada = data.tipo === "seleccion_multiple" ? opciones[index] : opcion;
            // Habilitar el botón "Continuar"
            nextBtn.disabled = false;
        });
    });   

    questionContainer.appendChild(opcionesContainer)
    contenedor.appendChild(questionContainer)

    nextBtn.textContent = (preguntaActual === totalPreguntas) ? "Finalizar" : "Continuar";
    nextBtn.disabled = !(respuestaSeleccionada !== "");

    // Evitar múltiples listeners acumulados
    if (nextButtonHandler) {
        nextBtn.removeEventListener("click", nextButtonHandler);
    }

    nextButtonHandler = () => handleNextButtonClick(data, respuestaSeleccionada);
    nextBtn.addEventListener("click", nextButtonHandler);
}

// Define el listener de forma global
function handleNextButtonClick(data, respuestaSeleccionada) {
    document.getElementById("bloqueo-interaccion").style.display = "block";

    const tiles = document.querySelectorAll(".radio-tile");
    tiles.forEach(tile => {
        const textoOpcion = tile.querySelector(".radio-label");
        tile.classList.remove("correcto", "error");

        if (textoOpcion.textContent === respuestaSeleccionada || textoOpcion.dataset.answer === respuestaSeleccionada) {
            if (respuestaSeleccionada.toLowerCase() === data.respuesta_correcta.toLowerCase()) {
                tile.classList.add("correcto");
                confetti();
                gameSoundAudio.src = "/static/assets/audio/gameSound/confetti.mp3";
                gameSoundAudio.play();
            } else {
                tile.classList.add("error");
                gameSoundAudio.src = "/static/assets/audio/gameSound/wrong.mp3";
                gameSoundAudio.play();
                preguntasIncorrectas.push([data.texto, respuestaSeleccionada]);
            }
        }
    });

    setTimeout(() => {
        document.getElementById("bloqueo-interaccion").style.display = "none";

        if (preguntaActual < totalPreguntas) {
            preguntaActual++;
            cargarPregunta(preguntaActual);
        } else {
            finalizarActividad();
        }
    }, 4000);
}

function actualizarBarraProgreso() {
    const progreso = (preguntaActual / totalPreguntas) * 100;
    progressFill.style.width = `${progreso}%`;
    progressText.textContent = `${progreso}%`;
}

function finalizarActividad() {
    //Ocultar quiz
    quizContainer.classList.add("hide")
    setTimeout(() => {
        quizContainer.style.display = "none";
        result.style.display = "grid";
        setTimeout(() => {
            result.classList.remove("hide");
        }, 300);
    }, 1000);

    restartActivityBtn.href = window.location.href;

    //Calcular puntaje
    const preguntasCorrectas = parseInt(totalPreguntas - preguntasIncorrectas.length);
    const puntaje = preguntasCorrectas * valorPorPregunta;
    const notaCualitativa = puntaje >= 3.5 ? "aprobado" : "reprobado";

    //Mostrar resultado
    resultImg.src = resultContent[notaCualitativa].img
    resultTitle.textContent = resultContent[notaCualitativa].title
    resultMessage.textContent = resultContent[notaCualitativa].text
    resultGrade.textContent = `${notaCualitativa.toUpperCase()} (Nota: ${puntaje})`;
    resultCorrect.textContent = `${preguntasCorrectas}/${totalPreguntas}`
    resultIncorrect.textContent = `${preguntasIncorrectas.length}/${totalPreguntas}`

    //Insertar calificacion a la db
    fetch('/estudiantes/insertarCalificacion/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            actividad_id: id,
            puntaje: puntaje.toFixed(1),
            notaCualitativa: notaCualitativa
        })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.mensaje) {
            Swal.fire({
                title: "¡Error!",
                text: `¡Ha ocurrido un error registrando la calificación! ${data}`,
                icon: "error"
            });
            setTimeout(() => window.location.reload(), 200000);
        }
    })
    .catch(error => {
        Swal.fire({
            title: "¡Error!",
            text: `¡Ha ocurrido un error durante la petición!`,
            icon: "error"
        });
        setTimeout(() => window.location.reload(), 200000);
    });
}

// función para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const trimmed = cookie.trim();
            if (trimmed.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}