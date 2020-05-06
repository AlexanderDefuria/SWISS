// I fucked your mom


var Slug = 0;

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