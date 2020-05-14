let avgChartName = 'avg_balls';
let totalChartName ='line';
let avgChart;
let totalChart;
let teamData = {};

document.addEventListener('DOMContentLoaded', function () {
    avgChart = Highcharts.chart(avgChartName, constCharts.avgChart);
    totalChart = Highcharts.chart(totalChartName, constCharts.totalChart)
    updateGlance()
});

function updateGlance() {

	$.ajax({
        // url: 'update/', -- TODO replace line below when slug is in the url
        url: 'update/',
        method: 'GET',
		dataType: "json",
        success: function(data) {
            teamData = JSON.parse(data.content)
			console.log(teamData);
		},
        failure: function () {
            console.log("Failed");

        },

    });
}
