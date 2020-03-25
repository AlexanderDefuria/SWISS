// Get the elements with class="column"
var elements = document.getElementsByClassName("column");

// Declare a loop variable
var i;


four();

// Full-width images
function one() {
  elements = document.getElementsByClassName("column");
  for (i = 0; i < elements.length; i++) {
    elements[i].style.flex = "100%";
  }
}

// Two images side by side
function two() {
  elements = document.getElementsByClassName("column");
  for (i = 0; i < elements.length; i++) {
    elements[i].style.flex = "49%";
  }
}

// Four images side by side
function four() {
  for (i = 0; i < elements.length; i++) {
    elements[i].style.flex = "24%";
  }
}

// Add active class to the current button (highlight it)
var header = document.getElementsByClassName("header")[0];
var btns = header.getElementsByClassName("btn");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}