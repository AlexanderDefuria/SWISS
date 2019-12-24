
var values = {
    third_cargo: 0,
    second_cargo: 0,
    first_cargo: 0,
    ship_cargo: 0,
    ship_hatch: 0,
    first_hatch: 0,
    second_hatch: 0,
    third_hatch: 0,
    time: 0,
    match_good: false,
};

function checkMatch(){

    $.ajax({
        url: 'check/',
        type: 'post',
        data: {
            'match_number': document.getElementById("match_number").value,
        },
        dataType: "json",
        success: function (data) {
            values['match_good'] = $.parseJSON(data.content)['result'];
            if (values['match_good']) console.log("Match number is acceptable")
            else window.alert("Please Confirm The Match Number")
        },
        failure: function (data) {
            console.log("No Match Confirmation");
        },

    });

}


function add(name, max)  {
    if(values[name] >= max) values[name] = max;
    else values[name] += 1;
    document.getElementById(name.concat('-label')).innerHTML = values[name];
    document.getElementById(name).value = values[name];
}
function subtract(name, min) {
    if(values[name] <= min) values[name] = min;
    else values[name] -= 1;
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


    if (value !== -1) {
        document.getElementById("starting_level").value = "2";
    }

}

var on = false;
var startTime;

function toggleTimer(elementID){
    if (on === false){
        startTime = Date.now();
        on = true;
        document.getElementById(elementID).style.backgroundColor = "lightcoral";
        document.getElementById(elementID).textContent = "Stop Timing Defense";

    } else {
        values['time'] += Date.now() - startTime;
        on = false;
        document.getElementById(elementID).style.backgroundColor = "lightgreen";
        document.getElementById(elementID).textContent = "Resume Defense Timer";
    }



}
function checkInputValues(mandatory_list) {

    var pass = true;

    if (!values['match_good']){
        pass = false;
        document.getElementById('match_number').style.backgroundColor = "red";
    }

    if (mandatory_list !== undefined )
        for (var i = 0; i < mandatory_list.length; i++){

            var element = document.getElementById(mandatory_list[i]);

            if(element.value === element.defaultValue){
                var indicate_list = document.getElementsByClassName(element.className);

                for (var x = 0; x < indicate_list.length; x++) {
                    document.getElementById(indicate_list[x].id).style.backgroundColor = "red";
                    document.getElementById(indicate_list[x].id).style.borderColor = "red";
                }

                pass = false;
            }
        }


    if (pass) {
        console.log("Success");
        document.getElementById("form").submit()
    } else {
        console.log("Failed Input");
        window.scrollTo(0,0)
    }


}
