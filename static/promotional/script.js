// JavaScript Document

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
		document.getElementById("navBar").classList.add("scrolled");
		document.getElementById("heroImage").style.opacity = "0.6";
  } else {
        document.getElementById("navBar").classList.remove("scrolled");
        document.getElementById("heroImage").style.opacity = "1";
  }
}

function openNav() {
	document.getElementById("sideNav").style.width="250px";
	document.getElementById("swissLogo").style.marginLeft="215px";
}
function closeNav() {
	document.getElementById("sideNav").style.width = "0";
	document.getElementById("swissLogo").style.marginLeft= "0";
}
