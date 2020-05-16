// Javascript file for various functions across ALL pages in SWISS. 


//Functions that control the Side Navbar on all pages
function openNav() {
	document.getElementById("sideNav").style.width="250px";
	document.getElementById("bodyContainer").style.marginLeft="275px";
	document.getElementById("swissLogo").style.marginLeft="215px";
}
function closeNav() {
  document.getElementById("sideNav").style.width = "0";
  document.getElementById("bodyContainer").style.marginLeft= "0";
  document.getElementById("swissLogo").style.marginLeft= "0";
}

//Function that controls the team number filtering on the data page. 

function tableFilter() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("teamNumber");
  filter = input.value.toUpperCase();
  table = document.getElementById("dataTable");
  tr = table.getElementsByTagName("tr");

for (i = 0; i < tr.length; i++) {
	td = tr[i].getElementsByTagName("td")[0];
	if (td) {
		txtValue = td.textContent || td.innerText;
		if (txtValue.toUpperCase().indexOf(filter) > -1) {
			tr[i].style.display = "";
		} else {
			tr[i].style.display = "none";
		}
	}
	}
	}

// Function that controls the team select drawer

function openTeamDrawer() {
	document.getElementById("teamDrawer").style.height="100%";
}
function closeTeamDrawer() {
  document.getElementById("teamDrawer").style.height = "0";
}


// Function that operates the increment and decrement buttons and logs any changes for Scouting pages

function incrementValue(id) {
	console.log(id)
	var value = parseInt(document.getElementById(id).value, 10);
	value = isNaN(value) ? 0 : value;
	value++;
	document.getElementById(id).value = value;
}
function decrementValue(id) {
	console.log(id)
	var value = parseInt(document.getElementById(id).value, 10);
	if (value <= 0)
		value = 0;
	else if (value >= 10)
		value = 10;
	else
			value--;
	document.getElementById(id).value = value;
}
function registerChange() {
	console.log();
}


// General script functions doing exactly what their names state

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
