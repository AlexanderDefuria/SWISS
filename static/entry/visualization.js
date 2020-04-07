let myChart;

document.addEventListener('DOMContentLoaded', function () {

    myChart = Highcharts.chart('container', constCharts.chartA);





});


function updateGraph(){

    $.ajax({
        url: 'update/',
        method: 'GET',
        dataType: "json",
        success: function(data) {
            updateChart()
        },
        failure: function (data) {
            console.log("Failed");

        },

    });

}


function select(element) {
    if (document.getElementById(element.id + 'IN').value === 'true'){
        document.getElementById(element.id + 'IN').value = false;
        element.style.opacity = '0.5';
    }
    else {
        document.getElementById(element.id + 'IN').value = true;
        element.style.opacity = '1';
    }

}

function updateChart() {
    myChart.update(constCharts.chartB);
}




