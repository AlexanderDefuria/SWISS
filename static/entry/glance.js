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
        // url: 'update/', -- TODO replace line below when slug is in the url
        url: 'update/',
        method: 'POST',
        data: {"team_id": team_id},
        dataType: "json",
        success: function (data) {
            teamData = JSON.parse(data.content)
        },
        failure: function () {
            console.log("Failed");

         },

    }).then(r => {
        // Total Line Chart
        constCharts.totalChart.series[0].data = []
        teamData.forEach( function (info, index) {
            constCharts.totalChart.series[0].data[index] = info["fields"]["outer"]
            constCharts.totalChart.series[0].data[index] += info["fields"]["lower"]
            constCharts.totalChart.series[0].data[index] += info["fields"]["inner"]
            constCharts.totalChart.series[0].data[index] += info["fields"]["outer_auto"]
            constCharts.totalChart.series[0].data[index] += info["fields"]["lower_auto"]
            constCharts.totalChart.series[0].data[index] += info["fields"]["inner_auto"]
        });
        totalChart = Highcharts.chart(totalChartName, constCharts.totalChart);
        totalChart.redraw()

        // Average Bar Graph
        if (!teamData.length < 1) {
            constCharts.avgChart.series[0].data = []
            let result = {};
            teamData.forEach( function (info, index) {
                result["lower"] = info["fields"]["lower"]
                result["outer"] = info["fields"]["outer"]
                result["inner"] = info["fields"]["inner"]
                result["lower_auto"] = info["fields"]["lower_auto"]
                result["outer_auto"] = info["fields"]["outer_auto"]
                result["inner_auto"] = info["fields"]["inner_auto"]
            });

            for (var x in result){
                result[x] /= teamData.length
            }

            constCharts.avgChart.series[0].data[0] = result['lower_auto']
            constCharts.avgChart.series[0].data[1] = result['lower']
            constCharts.avgChart.series[1].data[0] = result['outer_auto']
            constCharts.avgChart.series[1].data[1] = result['outer']
            constCharts.avgChart.series[2].data[0] = result['inner_auto']
            constCharts.avgChart.series[2].data[1] = result['inner']

            console.log(result)

            avgChart = Highcharts.chart(avgChartName, constCharts.avgChart);
            avgChart.redraw()
        }



    });
}
