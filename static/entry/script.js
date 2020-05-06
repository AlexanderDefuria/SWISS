// I fucked your mom

function autolowgoaladd() {
	document.getElementById("autoLowGoal").stepUp();
}

let Slug = 0;


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