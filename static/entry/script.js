// I fucked your mom


var Slug = 0;
var initialBoxID = 'MetricCheckBox';
let myChart;

document.addEventListener('DOMContentLoaded', function () {
    myChart = Highcharts.chart('visualizationChart', constCharts.chartA);
    // Loads all fields and starts the drag drop js
    getFields();
});
function getFields() {
	$.ajax({
        url: 'update/fields',
        method: 'GET',
		dataType: "json",
        success: function(data) {
			fieldData = JSON.parse(data.content);
			loadFields();
		},
        failure: function (data) {
            console.log("Failed");

        },

    });
}
function loadFields() {
    let keys = Object.keys(fieldData);
    for (let i = 0; i < keys.length; i++) {
        if (fieldData[keys[i]]["visible"]) {
            let node = document.createElement("DIV");
            node.classList.add("teamnumberPill");
            node.style.width = "auto";

            let inputNode = document.createElement("INPUT");
            inputNode.setAttribute("type", "checkbox");
            inputNode.id = fieldData[keys[i]]["alias"];
            inputNode.name = fieldData[keys[i]]["alias"];
            inputNode.style.marginRight = "5px";

            let labelNode = document.createElement("LABEL");
            labelNode.setAttribute("for", fieldData[keys[i]]["alias"]);
            labelNode.innerHTML = fieldData[keys[i]]["alias"];
            labelNode.style.marginLeft = "5px";

            node.appendChild(labelNode);
            node.appendChild(inputNode);
            node.id = keys[i];
            document.getElementById(initialBoxID).appendChild(node);
        }
    }


}
function updateGraph() {
    let fieldList = [];
    let teamList = [];


    let included = document.getElementById("included_fields");
    included = included.getElementsByTagName("LI");
    for (let i = 0; i < included.length; i++){
        fieldList.push(included[i].id)
    }

    included = document.getElementsByName("teamCheckBox")
    for (let i = 0; i < included.length; i++){
        if (included[i].checked)
            teamList.push(included[i].id);
    }

    let formData = new FormData();
    formData.append('field_list', fieldList);
    formData.append('team_list', teamList);
    formData.append('graphType', document.getElementById("graphType").value)

    let returnData = {};


    $.ajax({
        url: 'update/',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,

        success: function (data) {
            returnData = JSON.parse(data.content)
            // console.log(returnData);
        },
        failure: function (data) {
            console.log("Failed");
        },

    }).then(r =>{

        let fields = Object.keys(returnData[Object.keys(returnData)[0]])
        let teams = Object.keys(returnData)

        varChart.series = []

        fields.forEach(function (field, findex) {

            let data = []
            teams.forEach(function (team, tindex) {
                data.push(returnData[team][field] * fieldData[field]['weight'] * fieldData[field]['points'])
            });

            varChart.series.push({
                name: fieldData[field]["alias"],
                data: data
            })

        });

        varChart.xAxis.categories = teams;
        varChart.yAxis.title.text = 'Total Points'
        varChart.title.text = ''


        console.log(varChart.series)

        myChart = Highcharts.chart('container', varChart);

    });

}
function getCSV(json) {
	return $.ajax({
        url: 'getcsv/',
        type: 'post',
        data: {},
        dataType: "json",
        success: function (data) {
            console.log(data.content);
        },
        failure: function () {
            console.log("No Matches");
        },
    })
}
function getSlug(team) {
	return $.ajax({
        url: 'getslug/',
        type: 'post',
        data: {
            'team_number': document.getElementById("teamNumber").value,
        },
        dataType: "json",
        success: function (data) {
            Slug = $.parseJSON(data.content)['slug'];
        },
        failure: function (data) {
            console.log("No Match Confirmation");
        },

    });
}
function updateSlug(team){
	getSlug(team)
	return Slug
}