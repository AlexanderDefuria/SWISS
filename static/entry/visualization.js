let myChart;

document.addEventListener('DOMContentLoaded', function () {
    myChart = Highcharts.chart('container', constCharts.chartA);
    // Loads all fields and starts the drag drop js
    getFields();
});


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

function selectAllTeams(callerID) {
    let parent = document.getElementById(callerID).parentElement;
    let team_list = parent.getElementsByClassName('team_check');
    for (let i = 0; i < team_list.length; i++){
        let input = team_list[i].getElementsByTagName("input");
        input.item(0).checked = !input.item(0).checked;
    }
}

function getFields() {
	$.ajax({
        url: 'update/fields',
        method: 'GET',
		dataType: "json",
        success: function(data) {
			fieldData = JSON.parse(data.content);
			loadFields();
			initDragDropScript();
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
            let node = document.createElement("LI");
            let textNode = document.createTextNode(fieldData[keys[i]]["alias"]);
            node.appendChild(textNode);
            node.id = keys[i];
            document.getElementById(initialBoxID).appendChild(node);
        }
    }
    let element = document.getElementById('placeholder');
    element.parentNode.removeChild(element);

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
