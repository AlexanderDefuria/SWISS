
var values = {
    ThirdRocketCargo: 0,
    SecondRocketCargo: 0,
    FirstRocketCargo: 0,
    CargoShipCargo: 0,
    CargoShipHatch: 0,
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
    var cargo_button = document.getElementById( "cargo_button")
    var hatch_button = document.getElementById( "hatch_button")


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

function setAllianceColour(colour){


}