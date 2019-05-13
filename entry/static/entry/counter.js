
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

function selectLevel(elementID, class_name, value, toassign){
    var element_list = document.getElementsByClassName(class_name);

    for (var i = 0; i < element_list.length; i++){
        console.log(element_list[i]);
        element_list[i].style.opacity = "0.3";
        element_list[i].value = "";
        element_list[i].style.backgroundColor = "";
    }

    var x = document.getElementById(elementID);
    x.style.opacity = "1";
    x

    if (value !== -1) {
        document.getElementById("StartingLevel").value = "2";
    }

}

var on = false;
var startTime;
var time = 0;

function toggleTimer(elementID){
    if (on === false){
        startTime = Date.now();
        on = true;
        document.getElementById(elementID).style.backgroundColor = "lightcoral";
        document.getElementById(elementID).textContent = "Stop Timing Defense";

    } else {
        time += Date.now() - startTime;
        on = false;
        document.getElementById(elementID).style.backgroundColor = "lightgreen";
        document.getElementById(elementID).textContent = "Resume Defense Timer";
    }



}

function checkInputValues(mandatory_list) {

    var pass = true;

    for (var i = 0; i < mandatory_list.length; i++){

        var element = document.getElementById(mandatory_list[i]);

        if(element.value === element.defaultValue){
            var indicate_list = document.getElementsByClassName(element.className)

            for (var x = 0; x < indicate_list.length; x++) {
                document.getElementById(indicate_list[x].id).style.backgroundColor = "red";
                document.getElementById(indicate_list[x].id).style.borderColor = "red";
            }

            pass = false;
        }
    }

    // TODO re-enable the check, disabled to speed up internal testing
    if (true) {
        console.log("Success");
        document.getElementById("form").submit()
    } else {
        console.log("Failed Input");
        window.scrollTo(0,0)
    }


}
