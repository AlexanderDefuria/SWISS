document.addEventListener("DOMContentLoaded", function () {
	let modal = document.getElementById("myModal");
	let opn = document.getElementById("on_field_false"); // Button to open the modal
	let bad = document.getElementById("onFieldCancel"); // Cancel setting robot to off field
	let good = document.getElementById("onFieldConfirm"); // Indeed set robot to off field
	let main = document.getElementById("mainForm");
	let mod_head = document.getElementById("modal-header");
	let mod_desc = document.getElementById("modal-desc");

	// When the user clicks on the button, open the modal
	opn.onclick = function() {
		modal.style.visibility = "visible";
		main.style.filter="blur(2px)";
		const canVibrate = window.navigator.vibrate;
		if (canVibrate) window.navigator.vibrate(40);
    	mod_head.innerHTML="Are you sure the Robot is not Present?";
    	mod_desc.innerHTML="Clicking yes will set all form values to ZERO and scroll you to the bottom of the page."
	}

	// When the user clicks on "no", close the modal
	bad.onclick = function() {
	    closeModal();
	}

	// When the user clicks anywhere outside the modal, close it
	window.onclick = function(event) {
	  if (event.target === modal) {
	    closeModal();
	  }
	}

	// TODO What does this do?
	good.onclick = function() {
		modal.style.visibility = "hidden";
		const canVibrate = window.navigator.vibrate
		if (canVibrate) window.navigator.vibrate(40)
		main.style.filter="blur(0)";

		// TODO Setting all values to default should be done in backend (except Y/N).

		// Fill in required Y/N Inputs as N.
		for (let group of document.getElementsByClassName("radioGroup")) {
			group.children.item(1).children.item(1).checked=true;
			group.children.item(0).children.item(1).checked=false;
		}

		// Scroll to bottom
		setTimeout(() => { document.getElementById("submit").scrollIntoView({behavior: 'smooth'	}); }, 500);
	}

	function closeModal() {
		modal.style.visibility = "hidden";
		document.getElementById("on_field_false").checked = false;
		document.getElementById("on_field_true").checked = true;
		main.style.filter="blur(0)";
		const canVibrate = window.navigator.vibrate
		if (canVibrate) window.navigator.vibrate(40)
	}
});








