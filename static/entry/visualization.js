let myChart;

document.addEventListener('DOMContentLoaded', function () {

    myChart = Highcharts.chart('container', constCharts.chartA);

    // Loads all fields and starts the drag drop js
    getFields();


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



function selectAllTeams(callerID) {
    let parent = document.getElementById(callerID).parentElement;
    let team_list = parent.getElementsByClassName('team_check');
    for (let i = 0; i < team_list.length; i++){
        let input = team_list[i].getElementsByTagName("input");
        input.item(0).checked = !input.item(0).checked;
    }
}


function getFields()
{
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
        let node = document.createElement("LI");
        let textNode = document.createTextNode(fieldData[keys[i]]["alias"]);
        node.appendChild(textNode);
        node.id = keys[i];
        document.getElementById(initialBoxID).appendChild(node);
    }
    let element = document.getElementById('placeholder');
    element.parentNode.removeChild(element);

}

function fields() {
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


    $.ajax({
        url: 'update/',
        method: 'POST',
		data: formData,
        processData: false,
        contentType: false,

        success: function(data) {
			console.log(data)
		},
        failure: function (data) {
            console.log("Failed");
        },

    });


}
