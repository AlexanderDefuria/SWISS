// Javascript file for various functions across ALL pages in SWISS. 


//Functions that control the Side Navbar on all pages
function openNav() {
	document.getElementById("sideNav").style.width="250px";
	document.getElementById("swissLogo").style.marginLeft="215px";
	document.getElementById("bodyContainer").style.marginLeft="275px";
}
function closeNav() {
	document.getElementById("sideNav").style.width = "0";
	document.getElementById("swissLogo").style.marginLeft= "0";
	document.getElementById("bodyContainer").style.marginLeft= "0";
}

//Function that controls the bottom bar
function expandBottomBar() {
	document.getElementById("bottomBar").style.height = "70px";
	document.getElementById("bottomBarButton").style.height = "70px";
	document.getElementById("bottomBarButton").onclick = function () {collapseBottomBar()};
	document.getElementById("bottomBarContent").style.visibility = "visible";
	document.getElementById("bodyContainer").style.paddingBottom = "0px";
}	
function collapseBottomBar() {
	document.getElementById("bottomBar").style.height = "30px";
	document.getElementById("bottomBarButton").style.height = "30px";
	document.getElementById("bottomBarContent").style.visibility = "hidden";
	document.getElementById("bodyContainer").style.paddingBottom = "20px";
	document.getElementById("bottomBarButton").onclick = function () {expandBottomBar()};
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

function teamFilter(field) {
	let filter = document.getElementById(field).value.toString();
	let all = document.getElementsByClassName('teamLink')
	if (field === "teamNumber") {
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
//	document.getElementById("bodyContainer").style.filter="blur(4px)"
//  commented out -- causes poor performance on low resource devices 
}
function closeTeamDrawer() {
	document.getElementById("teamDrawer").style.height = "0";
//	document.getElementById("bodyContainer").style.filter="blur(0px)"
//  commented out -- causes poor performance on low resource devices 
}


// Function that operates the increment and decrement buttons and logs any changes for Scouting pages

function incrementValue(id) {
	console.log(id)
	var value = parseInt(document.getElementById(id).value, 10);
	value = isNaN(value) ? 0 : value;
	value++;
	document.getElementById(id).value = value;
	window.navigator.vibrate(40);
}
function incrementPreload(id) {
	console.log(id)
	var value = parseInt(document.getElementById(id).value, 10);
	if (value >= 3) {
		value = 3;
		window.navigator.vibrate([30,20,30,20,30]);
	}	else	{
			value++;
		window.navigator.vibrate(40);
	}
	document.getElementById(id).value = value;
}
function decrementValue(id) {
	console.log(id)
	var value = parseInt(document.getElementById(id).value, 10);
	if (value <= 0) {
		value = 0;
		window.navigator.vibrate([30,20,30,20,30]);
	}	else	{
			value--;
		window.navigator.vibrate(40);
	}
	document.getElementById(id).value = value;
}
function registerChange() {
	console.log();
	window.navigator.vibrate(40);
}
// General script functions doing exactly what their names state

var Slug = 0;

function getCSV(json) {
var x = document.getElementById("snackbar");
var y = document.getElementById("snacktext");
	return $.ajax({
        url: 'getcsv/',
        type: 'post',
        data: {},
        dataType: "json",
        success: function (data) {
            console.log(data.content);
			x.className = "show";
			y.innerHTML = "Match Data Downloading...";
			setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
        },
        failure: function () {
            console.log("No Matches");
			x.className = "show";
			y.innerHTML = "Error: No Matches!";
			setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
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

//////////////////////////////////////////////////////////////////////////
//          SCRIPT FOR HANDLING THE ADD TO HOME SCREEN EXPERIENCE!      //
//////////////////////////////////////////////////////////////////////////

let deferredPrompt;
const addBtn = document.querySelector('.add-button')
addBtn.style.display = 'none';

window.addEventListener('beforeinstallprompt', (e) => {
	// This prevents Chrome 67 and earlier from automatically showing the prompt 
	e.preventDefault();
	// Stashed the event so it can be triggered later 
	deferredPrompt = e;
	// Uodate UI to notified the user they can add to home screen 
	addBtn.style.display = 'block';
	
	addBtn.addEventListener('click', (e) => {
		// hide our user interface that shows the add to home button 
		addBtn.style.display = 'none';
		// Show the prompt 
		deferredPrompt.prompt();
		// Wait for reponse to the prompt 
		deferredPrompt.userChoice.then((choiceResult) => {
			if (choiceResult.outcome === 'accepted') {
				console.log('User accepted the A2HS prompt');
			} else { 
				console.log('User dismissed the A2HS prompt');
			}
			deferredPrompt = null; 
		});
	});
});


