const aprobados = parseInt(document.querySelector("#aprobados").value);
const desaprobados = parseInt(document.querySelector("#desaprobados").value);
const chartSection = document.querySelector(".chart__section");
const table = document.querySelector(".table");
const notFoundSection = document.querySelector(".not__found")

if (aprobados !== 0 && desaprobados !== 0) {
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Aprobados', 'Reprobados'],
            datasets: [{
            data: [aprobados, desaprobados],
            backgroundColor: ['#4BC0C0', '#FF6384'],
            hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            plugins: {
            legend: {
                position: 'bottom',
                labels: {
                color: '#444',
                font: {
                    size: 14
                }
                }
            },
            tooltip: {
                backgroundColor: '#222',
                titleColor: '#fff',
                bodyColor: '#fff'
            }
            },
            cutout: '60%' // hace que sea tipo doughnut
        }
    });
}else{
    //En caso de que no haya respuestas se ocultan
    chartSection.style.display = "none";
    table.style.display = "none";
    notFoundSection.classList.remove("hide");
}