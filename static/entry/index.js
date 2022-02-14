document.addEventListener("DOMContentLoaded", function (){

var x = document.getElementById("alertbar");
		var y = document.getElementById("alerttext");
		var z = document.getElementById("tutorialCookie").innerHTML;

		document.addEventListener('DOMContentLoaded', function () {
			setTimeout(function () {
				if (z == "False") {
					x.className = "show";
					y.innerHTML = "Welcome to SWISS! Do you want a walkthrough?";
                    console.log("Tutorial Prompt On");
				} else if (z == "True") {
					console.log("Tutorials Off")
				} else {
					x.className = "show";
					y.innerHTML = "Welcome to SWISS! Do you want a walkthrough?";
					console.log("No Tutorial Prompt Cookie set");
				}
			}, 500), false
		})

        var modal = document.getElementById("myModal");
        var opn = document.getElementById("tileDownload");
        var bad = document.getElementById("downloadCancel");
        var good = document.getElementById("downloadConfirm");
        var main = document.getElementById("tileContainer");
        var modhead = document.getElementById("modal-header");
        var moddesc = document.getElementById("modal-desc");

        // When the user clicks on the button, open the modal
        opn.onclick = function() {
            modal.style.visibility = "visible";
            main.style.filter = "blur(2px)";
            window.navigator.vibrate(40);
            modhead.innerHTML = "Download Match Data?";
            moddesc.innerHTML = "All match data for current event will be downloaded in a CSV format.";
        }

        // When the user clicks on "no", close the modal
        bad.onclick = function() {
            modal.style.visibility = "hidden";
            main.style.filter="blur(0)";
            window.navigator.vibrate(40);
        }

        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
          if (event.target == modal) {
            modal.style.visibility = "hidden";
            main.style.filter = "blur(0)";
            window.navigator.vibrate(40);
          }
        }

        good.onclick = function() {
        // When the user clicks "ok", href to download link
            document.location='./download';
        }

});
