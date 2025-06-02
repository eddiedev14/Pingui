//Evento para añadir una nueva pregunta
const form = document.querySelector("#activity");
const materiaSelect = document.querySelector("#materia");
const tematicaSelect = document.querySelector("#tematica");
const addNewQuestionBtn = document.querySelector(".form__button--secondary");
const notyf = new Notyf({
    duration: 2000,
    position: {
        x: 'right',
        y: 'top',
    },
});
let contadorPreguntas = 0;
const url = window.location.href;
const segments = url.split("/").filter(Boolean); // elimina elementos vacíos
const id = segments[segments.length - 1];
const esIdValido = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id);;  // Solo es válido si es un número

//Se obtiene la cookie de csrf para poder enviar el form
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

//Evento para mostrar solo las tematicas asociadas a cada materia
materiaSelect.addEventListener("change", e => {
    const materiaId = e.target.value;

    // Limpia temáticas actuales
    tematicaSelect.innerHTML = '<option value="">Selecciona una opción</option>';

    if (materiaId) {
        fetch(`/obtener-tematicas/?materia_id=${materiaId}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(t => {
                    const option = document.createElement("option");
                    option.value = t.id;
                    option.textContent = t.nombre;
                    tematicaSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error("Error al cargar temáticas:", error);
            });
    }
});

//Evento para añadir nueva pregunta
addNewQuestionBtn.addEventListener("click", () => {
    contadorPreguntas++;
    const template = document.querySelector('#question__template');
    const question = template.content.cloneNode(true);

    // Añadir manejador al botón "Eliminar" del clon
    question.querySelector('.activity__btn--delete').addEventListener('click', deleteQuestion);

    //Agregamos eventos
    question.querySelector(".activity__btn--upload").addEventListener("click", openFile)
    question.querySelector("input[type='file']").addEventListener("change", notifyUpload)
    question.querySelector(".form__input--tipo_pregunta").addEventListener("change", handleQuestionType);

    form.appendChild(question);
    actualizarNumeros();
})

function deleteQuestion(e) {
    Swal.fire({
            icon: "question",
            title: "¿Deseas eliminar la pregunta seleccionada?",
            showCancelButton: true,
            confirmButtonText: "Eliminar",
            cancelButtonText: "Cancelar"
            }).then((result) => {
            if (result.isConfirmed) {
                e.target.closest('.activity__question').remove();
                actualizarNumeros();
            }
    });
}

function openFile(e) {
    const target = e.target;
    let label = target;

    if (target.nodeName === "I") {
        label = target.parentElement
    }

    const inputFile = label.parentElement.nextElementSibling;
    inputFile.click();
}

function actualizarNumeros() {
    const preguntas = form.querySelectorAll('.activity__question');
    preguntas.forEach((pregunta, index) => {
        const titulo = pregunta.querySelector('h2');
        titulo.textContent = `Pregunta #${index + 1}`;
    });
}

//Evento para cuando se cambie el tipo de pregunta
function handleQuestionType(e) {
    const container = e.target.closest(".question__form");
    const opcionesDiv = container.querySelector(".opciones");
    const divider = opcionesDiv.previousElementSibling;

    if (e.target.value === "verdadero_falso") {
        opcionesDiv.style.display = "none";
        divider.style.display = "none";
    } else {
        opcionesDiv.style.display = "grid";
        divider.style.display = "block";
    }
}

//Notificación cuando se sube imagen
document.querySelector("input[type='file']").addEventListener("change", notifyUpload)

function notifyUpload(e) {
    notyf.success('¡Imagen subida!');

    if (imagePreview) {
        const [file] = e.target.files

        if (file && e.target.id === "imagen_actividad") {
            imagePreview.src = URL.createObjectURL(file)
        }
    }
}

//Enviar formulario
form.addEventListener("submit", e => {
    e.preventDefault();

    // Obtener campos generales de la actividad
    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();
    const materia = document.getElementById("materia").value.trim();
    const tematica = document.getElementById("tematica").value.trim();
    const imagenActividadInput = document.getElementById("imagen_actividad");
    const imagenActividad = imagenActividadInput ? imagenActividadInput.files[0] : null;

    // Validar campos de actividad
    if (!nombre || !descripcion || !materia || !tematica || (!imagenActividad && !esIdValido)) {
        Swal.fire({
            title: "¡Error!",
            text: "¡Los campos de la actividad son obligatorios, hay campos vacíos! (Incluyendo la imagen)",
            icon: "error"
        });
        return;
    }

    const preguntas = [];
    let hayError = false;    

    document.querySelectorAll(".activity__question").forEach((preguntaDiv, index) => {
        const imagenPreguntaInput = preguntaDiv.querySelector("input[type='file']");
        const imagenPregunta = imagenPreguntaInput ? imagenPreguntaInput.files[0] : null;
        const tipoPregunta = preguntaDiv.querySelector(".form__input--tipo_pregunta").value.trim();
        const pregunta = preguntaDiv.querySelector(".form__input--pregunta").value.trim();
        const respuesta = preguntaDiv.querySelector(".form__input--respuesta").value.trim().toLowerCase();
        const questionId = preguntaDiv.dataset.questionid;

        if ((!imagenPregunta && !questionId) || !tipoPregunta || !pregunta || !respuesta) {
            Swal.fire({
                title: "¡Error!",
                text: `¡Completa todos los campos requeridos en la pregunta #${index + 1} (Incluyendo la imagen)!`,
                icon: "error"
            });
            hayError = true
            return;
        }

        //Valido que la respuesta de la pregunta sea valida
        if (tipoPregunta === "seleccion_multiple" && (respuesta !== "a" && respuesta !== "b" && respuesta !== "c" && respuesta !== "d")) {
            Swal.fire({
                title: "¡Error!",
                text: `¡La respuesta para la pregunta #${index + 1} de opción múltiple no es correcta, debe ser a, b, c o d!`,
                icon: "error"
            });
            hayError = true
            return;
        }else if(tipoPregunta === "verdadero_falso" && (respuesta !== "verdadero" && respuesta !== "falso")){
            Swal.fire({
                title: "¡Error!",
                text: `¡La respuesta para la pregunta #${index + 1} de verdadero_falso no es correcta, debe ser verdadero o falso!`,
                icon: "error"
            });
            hayError = true
            return;
        }

        const preguntaObj = { tipoPregunta, pregunta, respuesta };

        if (imagenPregunta) {
            preguntaObj.imagenPregunta = imagenPregunta;
        }

        if (tipoPregunta === "seleccion_multiple") {
            const opcion_a = preguntaDiv.querySelector(".form__input--opcion_a").value.trim();
            const opcion_b = preguntaDiv.querySelector(".form__input--opcion_b").value.trim();
            const opcion_c = preguntaDiv.querySelector(".form__input--opcion_c").value.trim();
            const opcion_d = preguntaDiv.querySelector(".form__input--opcion_d").value.trim();

            if (!opcion_a || !opcion_b || !opcion_c || !opcion_d) {
                Swal.fire({
                    title: "¡Error!",
                    text: `¡Completa todas las opciones en la pregunta #${index + 1}!`,
                    icon: "error"
                });
                hayError = true;
                return;
            }

            preguntaObj.opcion_a = opcion_a;
            preguntaObj.opcion_b = opcion_b;
            preguntaObj.opcion_c = opcion_c;
            preguntaObj.opcion_d = opcion_d;
        }

        //Si se esta editando y el container tiene id, se pasa en el objeto
        if (esIdValido && questionId) {
            preguntaObj.id = questionId;
        }

        preguntas.push(preguntaObj);
    });

    if (hayError) return;

    if (preguntas.length === 0) {
        Swal.fire({
            title: "¡Error!",
            text: `¡Ingresa por lo menos una pregunta para la actividad!`,
            icon: "error"
        });
        return;
    }

    // Separar las imágenes de las preguntas antes de enviar
    const preguntasSinImagenes = preguntas.map(({ imagenPregunta, ...resto }) => resto);

    const actividad = {
        id,
        nombre,
        descripcion,
        materia,
        tematica,
        preguntas: preguntasSinImagenes
    };

    console.log(preguntasSinImagenes)

    // Crear FormData
    const formDataEnviar = new FormData();
    formDataEnviar.append("actividad", JSON.stringify(actividad));
    
    if(imagenActividad) {
        formDataEnviar.append("imagenActividad", imagenActividad);
    }

    preguntas.forEach((p, i) => {
        if(p.imagenPregunta) { //Unicamente se manda la imagen si no tiene id (osea si no existe)
            formDataEnviar.append(`imagenPregunta_${i}`, p.imagenPregunta);
        }
    });

    if (!esIdValido) {
        // Enviar con fetch
        fetch("/profesores/actividades/create/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: formDataEnviar
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    title: "¡Felicitaciones!",
                    text: `¡La actividad ha sido creada correctamente!`,
                    icon: "success"
                });
                setTimeout(() => window.location.href = "/profesores/actividades/", 3000);
            } else {
                Swal.fire({
                    title: "Error",
                    text: `¡Ha ocurrido un error creando la actividad!`,
                    icon: "error"
                });
                setTimeout(() => window.location.href = "/profesores/actividades/", 3000);
            }
        })
    }else{
        // Enviar con fetch
        fetch(`/profesores/actividades/edit/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: formDataEnviar
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    title: "¡Felicitaciones!",
                    text: `¡La actividad ha sido actualizada correctamente!`,
                    icon: "success"
                });
                setTimeout(() => window.location.href = "/profesores/actividades/", 3000);
            } else {
                Swal.fire({
                    title: "Error",
                    text: `¡Ha ocurrido un error actualizando la actividad!`,
                    icon: "error"
                });
                setTimeout(() => window.location.href = "/profesores/actividades/", 3000);
            }
        })
    }
})

//* EDICION/VISUALIZACION DE ACTIVIDAD
const imagePreview = document.getElementById("image__preview");
const uploadQuestionImageBtn = document.querySelectorAll(".activity__btn--upload");
const inputFileQuestionImage = document.querySelectorAll(".file__imagen__pregunta")
const questionTypeSelects = document.querySelectorAll(".form__input--tipo_pregunta")
const questionDeleteBtns = document.querySelectorAll(".activity__btn--delete")

//* Añadimos eventos a selects de las preguntas, botones y inputs
uploadQuestionImageBtn.forEach(btn => btn.addEventListener("click", openFile))
questionTypeSelects.forEach(select => select.addEventListener("change", handleQuestionType))
questionDeleteBtns.forEach(btn => btn.addEventListener("click", deleteQuestion))
inputFileQuestionImage.forEach(input => input.addEventListener("change", notifyUpload))

//* Añadimos eventos y funciones para eliminar
const deleteActivityBtn = document.querySelector(".form__button--delete");
const archiveActivityBtn = document.querySelector(".form__button--archive");

if (deleteActivityBtn && archiveActivityBtn) {
    deleteActivityBtn.addEventListener("click", deleteActivity);
    archiveActivityBtn.addEventListener("click", archiveActivity)
}

function deleteActivity() {
    Swal.fire({
            icon: "question",
            title: "¿Deseas eliminar la actividad?",
            showCancelButton: true,
            confirmButtonText: "Eliminar",
            cancelButtonText: "Cancelar"
            }).then((result) => {
            if (result.isConfirmed) {
                // Enviar con fetch
                fetch(`/profesores/actividades/delete/${id}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire({
                            title: "¡Felicitaciones!",
                            text: `¡La actividad ha sido eliminada correctamente!`,
                            icon: "success"
                        });
                        setTimeout(() => window.location.href = "/profesores/actividades/", 3000);
                    }
                })
            }
    });
}

function archiveActivity() {
    Swal.fire({
            icon: "question",
            title: "¿Deseas archivar/desarchivar la actividad?",
            showCancelButton: true,
            confirmButtonText: "Sí, deseo hacerlo",
            cancelButtonText: "Cancelar"
            }).then((result) => {
            if (result.isConfirmed) {
                // Enviar con fetch
                fetch(`/profesores/actividades/archive/${id}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire({
                            title: "¡Felicitaciones!",
                            text: `¡La actividad ha sido ${data.accion} correctamente!`,
                            icon: "success"
                        });
                        setTimeout(() => window.location.href = "/profesores/actividades/", 3000);
                    }
                })
            }
    });
}