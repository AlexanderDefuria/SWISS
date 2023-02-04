// Below is Nick's select and deselect all buttons
function selectAll(name='teamCheckBox') {
	var items = document.getElementsByName(name);
	for (var i = 0; i < items.length; i++) {
		if (items[i].type === 'checkbox')
			items[i].checked = true;
	}
}

function unselectAll(name='teamCheckBox') {
	var items = document.getElementsByName(name);
	for (var i = 0; i < items.length; i++) {
		if (items[i].type === 'checkbox')
			items[i].checked = false;
	}
}	




var initialBoxID = 'MetricCheckBox';
let myChart;
let fieldData;

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
            node.onclick = function (event) {
                if (event.target.className === "teamnumberPill") {
                    event.target.childNodes[1].checked = !event.target.childNodes[1].checked ;
                } else if (event.target.tagName === "LABEL") {
                    event.target.parentNode.childNodes[1].checked = !event.target.parentNode.childNodes[1].checked ;
                } else {
                    console.log(event.target.tagName)
                }
            }

            let inputNode = document.createElement("INPUT");
            inputNode.setAttribute("type", "checkbox");
            inputNode.id = keys[i];
            inputNode.name = 'MetricCheckbox'//fieldData[keys[i]]["alias"];
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
function updateGraph(...args) {
    let fieldList = getActiveFields("MetricCheckBox");
    let teamList = getActiveFields("TeamCheckBox");
    let potentialArgs = ["Total", "Average"]

    let formData = new FormData();
    formData.append('field_list', fieldList);
    formData.append('team_list', teamList);
    formData.append('graphType', "bar")

	var x = document.getElementById("snackbar");
	var y = document.getElementById("snacktext");
	
    if (!fieldList.length > 0) {
        x.className = "show";
		y.innerHTML = "No Metrics are Selected!";
		setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
        return
    }
    else if (!teamList.length > 0) {
        x.className = "show";
		y.innerHTML = "No Teams are Selected!";
		setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
        return
    }
    // Below Code is designed to get the type of graph which determines the
    // return data and format in graphing.py def graph() function
    // presently hardcoded as a workaround TODO fix chart type selection
    // console.log(document.getElementById("visualizationChart").value)

    let returnData = {};

    $.ajax({
        url: 'update/',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,

        success: function (data) {
            returnData = JSON.parse(data.content)

        },
        failure: function (data) {
            console.log("Failed");
        },

    }).then(r => {

        let argDict = {}

        potentialArgs.forEach(function (potentialArg, paindex) {
            argDict[potentialArg] = args.includes(potentialArg);
        });


        let fields = Object.keys(returnData[Object.keys(returnData)[0]])
        console.log(fields)
        fields.forEach(function (field, findex) {
            if (!Object.keys(fieldData).includes(field)){
                let index = fields.indexOf(field)
                if (index > -1) {
                    fields.splice(index, 1)
                }
            }
        })


        let teams = Object.keys(returnData)

        let varChart = constCharts.templateChart;
        varChart.series = [];

        console.log(fields)

        fields.forEach(function (field, findex) {

            let data = []
            teams.forEach(function (team, tindex) {
                data.push(returnData[team][field] * fieldData[field]['weight'] * fieldData[field]['points'])
                if (argDict['Average'] && returnData[team]['MatchAmount'] > 0) {
                    data[data.length - 1] /= returnData[team]['MatchAmount'];
                    console.log(returnData[team][field])
                }
            });

            varChart.series.push({
                name: fieldData[field]["alias"],
                data: data
            })

        });

        varChart.xAxis.categories = teams;
        varChart.yAxis.title.text = 'Total Points'
        varChart.title.text = ''
        varChart.yAxis.plotLines = [{
            color: '#000000',
            width: 2,
            value: 0,
            zIndex: 10
        }]


       //  console.log(varChart.series)

        myChart = Highcharts.chart('visualizationChart', varChart);





    });

}