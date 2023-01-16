// Javascript file for various functions across ALL pages in SWISS. 

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

//Functions that control the Side Navbar on all pages
function openNav() {
	document.getElementById("sideNav").style.width="250px";
	document.getElementById("swissLogo").style.marginLeft="215px";
}
function closeNav() {
	document.getElementById("sideNav").style.width = "0";
	document.getElementById("swissLogo").style.marginLeft= "0";
}

//Function that controls the bottom bar
function expandBottomBar() {
	document.getElementById("bottomBarContent").style.visibility = "visible";
	document.getElementById("bottomBar").style.height = "auto";
	document.getElementById("bottomBarButton").style.height = "80px";
	document.getElementById("bottomBarButton").onclick = function () {collapseBottomBar()};
	document.getElementById("bodyContainer").style.paddingBottom = "0px";
}	
async function collapseBottomBar() {
	document.getElementById("bottomBarContent").style.visibility = "hidden";
	await sleep(200);
	document.getElementById("bottomBar").style.height = "30px";
	document.getElementById("bottomBarButton").style.height = "30px";
	document.getElementById("bodyContainer").style.paddingBottom = "20px";
	document.getElementById("bottomBarButton").onclick = function () {expandBottomBar()};
}


// Function that closes the alertbar

function closeAlertBar() {
    setTimeout(function () {
        setTimeout(function(){ x.className = x.className.replace("hide", ""); }, 450);
        x.className = "hide";
    }) 
}

// Function that controls the team number filtering on the data page. 

function tableFilter(field) {
  	var input, filter, table, tr, td, i, txtValue, index;
  	input = document.getElementById(field);
  	filter = input.value.toUpperCase();
  	table = document.getElementById("dataTable");
  	tr = table.getElementsByTagName("tr");

  	index = {"teamName": 1, "teamNumber": 0, "matchNumber": 2}

  	for (i = 0; i < tr.length; i++) {
  		td = tr[i].getElementsByTagName("td")[index[field]];
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

// Function that filters teamLink elements on Teams page by either team number or team name

function teamFilter(field) {
	let filter = document.getElementById(field).value.toString();
	let all = document.getElementsByClassName('teamLink')
	if (field === "teamSearch") {
		for (let i = 0; i < all.length; i++) {
			if (all[i].name.toString().toUpperCase().indexOf(filter.toString().toUpperCase()) > -1)
				all[i].style.display = "";
			else
				all[i].style.display = "none";
		}
	}
	document.getElementsByClassName("teamChip")
}

// Function that filter hour logs on Hours Log View page by student name 

function logFilter(field) {
	let filter = document.getElementById(field).value.toString();
	let all = document.getElementsByClassName('logChip')
	if (field === "studentName") {
		for (let i = 0; i < all.length; i++) {
			if (all[i].id.toString().indexOf(filter) > -1)
				all[i].style.display = "";
			else
				all[i].style.display = "none";

		}
	}
	document.getElementsByClassName("logChip")
}


// Function that filters schedule elements on Match Schedule page by match number


async function scheduleFilter(field) {
	let filter = document.getElementById(field).value.toString();
	let all = document.getElementsByClassName('scheduleLink');
	if (field === "matchNumber") {
		for (let i = 0; i < all.length; i++) {
			if (all[i].id.toString().indexOf(filter) > -1)
				all[i].style.display = "";
			else
				all[i].style.display = "none";

		}
	} else if (field === "teamName") {
		for (let i = 0; i < all.length; i++) {
			if (all[i].name.toString().toUpperCase().indexOf(filter.toString().toUpperCase()) > -1)
				all[i].style.display = "";
			else
				all[i].style.display = "none";
		}
	}
	document.getElementsByClassName("teamChip")
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
	var value = parseInt(document.getElementById(id).value, 10);
	value = isNaN(value) ? 0 : value;
	value++;
	document.getElementById(id).value = value;
	const canVibrate = window.navigator.vibrate
	if (canVibrate) window.navigator.vibrate(40)
	console.log(id);
}

function incrementPreload(idplus) {
	var x = document.getElementById("snackbar");
	var y = document.getElementById("snacktext");
	console.log(idplus);
	var value = parseInt(document.getElementById(idplus).value, 10);
	if (value >= 3) {
		value = 3;
		window.navigator.vibrate([30,20,30,20,30]);
		x.className = "show";
		y.innerHTML = "Maximum Preload Reached";
		setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
	}	else	{
			value++;
		window.navigator.vibrate(40);
	}
	document.getElementById(idplus).value = value;
}

function decrementValue(idminus) {
	var x = document.getElementById("snackbar");
	var y = document.getElementById("snacktext");
	var value = parseInt(document.getElementById(idminus).value, 10);
	if (value <= 0) {
		value = 0;
		const canVibrate = window.navigator.vibrate
		if (canVibrate) window.navigator.vibrate([30,20,30,20,30])
		x.className = "show";
		y.innerHTML = "Cannot have less than 0";
		setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
	}	else	{
			value--;
			const canVibrate = window.navigator.vibrate
			if (canVibrate) window.navigator.vibrate(40)
	}
	document.getElementById(idminus).value = value;
	console.log(idminus);
}

function registerChange() {
	window.navigator.vibrate(40);
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
