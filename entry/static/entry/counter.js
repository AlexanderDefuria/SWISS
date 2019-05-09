
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




function toggleInputDisplay(elementID, defaultStyle) {

    var cargo = document.getElementById(elementID + "_cargo");
    var hatch = document.getElementById(elementID + "_hatch");

    if (cargo.style.display === "none") {
        cargo.style.display = defaultStyle;
        hatch.style.display = "none";
    } else  {
        cargo.style.display = "none";
        hatch.style.display = defaultStyle;
    }


}