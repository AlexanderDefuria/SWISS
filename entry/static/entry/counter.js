
var values = {
    ThirdRocketCargo: 0,
    SecondRocketCargo: 0,
    FirstRocketCargo: 0,
    ShipCargo: 0,
    ShipHatch: 0,
    FirstRocketHatch: 0,
    SecondRocketHatch: 0,
    ThirdRocketHatch: 0,
};

function add(name)  {
    values[name] += 1;
    if(values[name] > 8) values[name] = 8;
    document.getElementById(name.concat('-label')).innerHTML = values[name];
    document.getElementById(name).value = values[name];
}

function subtract(name) {
    values[name] -= 1;
    if(values[name] < 0) values[name] = 0;
    document.getElementById(name.concat('-label')).innerHTML = values[name];
    document.getElementById(name).value = values[name];

}


function toggleInputDisplay(elementID, target, defaultStyle) {

    var cargo = document.getElementById(elementID + "_cargo");
    var hatch = document.getElementById(elementID + "_hatch");
    var cargo_button = document.getElementById( elementID + "_cargo_button")
    var hatch_button = document.getElementById( elementID + "_hatch_button")


    if (target === "cargo") {
        cargo.style.display = defaultStyle;
        cargo_button.style.opacity = "1";
        hatch.style.display = "none";
        hatch_button.style.opacity = "0.4";

    } else  if (target === "hatch") {
        cargo.style.display = "none";
        cargo_button.style.opacity = "0.4";
        hatch.style.display = defaultStyle;
        hatch_button.style.opacity = "1";
    }

}

function selectLevel(elementID, class_name){
    var element_list = document.getElementsByClassName("level");

    for (var i = 0; i < element_list.length; i++){
        console.log(element_list[i])
        element_list[i].style.opacity = "0.3";
    }

    var x = document.getElementById(elementID);
    x.style.opacity = "1";
}