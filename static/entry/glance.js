let avgChartName = 'avg_balls';
let totalChartName ='line';
let avgChart;
let totalChart;
let teamData = {};

document.addEventListener('DOMContentLoaded', function () {
    avgChart = Highcharts.chart(avgChartName, constCharts.avgChart);
    totalChart = Highcharts.chart(totalChartName, constCharts.totalChart)
    let pk = String(window.location.href).split("/")[String(window.location.href).split("/").length - 2]
    updateGlance(pk)
});

function updateGlance(team_id) {
	$.ajax({
        url: 'update/',
        method: 'POST',
        data: {"team_id": team_id},
        dataType: "json",
        success: function (data) {
            teamData = JSON.parse(data.content)
            console.log(teamData)
        },
        failure: function () {
            console.log("Failed");
        },

    }).then(r => {
        // Total Line Chart
        field = ["upper", "lower", "upper_auto", "lower_auto"]

        constCharts.totalChart.series[0].data = []
        teamData.forEach( function (info, index) {
            constCharts.totalChart.series[0].data[index] = 0
            field.forEach(function (field, indexb) {
                    constCharts.totalChart.series[0].data[index] += info["fields"][field]
                })
        });
        totalChart = Highcharts.chart(totalChartName, constCharts.totalChart);
        totalChart.redraw()

        // Average Bar Graph
        if (!teamData.length < 1) {
            constCharts.avgChart.series[0].data = []
            let result = {};

            field.forEach(function (field, index) {
                result[field] = 0
            })
            teamData.forEach( function (info, index) {
                field.forEach(function (field, index) {
                    result[field] += info["fields"][field]
                })
            });

            for (var x in result){
                result[x] /= teamData.length
            }

            // check chart.js to make sense of this and the indexes being referenced
            console.log(result)

            constCharts.avgChart.series[0].data[0] = result['upper_auto']
            constCharts.avgChart.series[0].data[1] = result['upper']
            constCharts.avgChart.series[1].data[0] = result['lower_auto']
            constCharts.avgChart.series[1].data[1] = result['lower']


            avgChart = Highcharts.chart(avgChartName, constCharts.avgChart);
            avgChart.redraw()
        }
    });
}
