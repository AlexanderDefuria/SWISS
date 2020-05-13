var initialBoxID = 'MetricCheckBox';
let myChart;

document.addEventListener('DOMContentLoaded', function () {
    myChart = Highcharts.chart('visualizationChart', constCharts.templateChart);
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
            inputNode.id = keys[i];
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
function getActiveFields(id) {
    let node = document.getElementById(id);
    let pills = node.childNodes;
    let activeFields = [];

    pills.forEach((pill) => {
        pill.childNodes.forEach((inner) => {
            if (inner.tagName === "INPUT")
                if (inner.checked)
                    activeFields.push(inner.id);
        });
    });

    //console.log(activeFields)

    return activeFields
}
function updateGraph() {
    let fieldList = getActiveFields("MetricCheckBox");
    let teamList = getActiveFields("TeamCheckBox");

    let formData = new FormData();
    formData.append('field_list', fieldList);
    formData.append('team_list', teamList);
    formData.append('graphType', "bar")

    // Below Code is designed to get the type of graph which determines the
    // return data and format in graphing.py def graph() function
    // presently hardcoded as a workaround TODO fix chart type selection
    //console.log(document.getElementById("visualizationChart").value)

    let returnData = {};

    $.ajax({
        url: 'update/',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,

        success: function (data) {
            returnData = JSON.parse(data.content)
            console.log(returnData);
        },
        failure: function (data) {
            console.log("Failed");
        },

    }).then(r => {

        let fields = Object.keys(returnData[Object.keys(returnData)[0]])
        let teams = Object.keys(returnData)

        let varChart = constCharts.templateChart;
        varChart.series = [];

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

        myChart = Highcharts.chart('visualizationChart', varChart);



    });

}