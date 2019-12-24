function updateImage(){

    $.ajax({
        url: 'update/',
        type: 'post',
        data: { 'type':             document.getElementById("GraphSelection").valueAsNumber,
                'team1':            document.getElementById("team1").valueAsNumber,
                'team2':            document.getElementById("team2").valueAsNumber,
                'team3':            document.getElementById("team3").valueAsNumber,
                'team4':            document.getElementById("team4").valueAsNumber,
                'team5':            document.getElementById("team5").valueAsNumber,
                'team6':            document.getElementById("team6").valueAsNumber,

                'total_hatch':       document.getElementById("total_hatchIN").value,
                'first_hatch':      document.getElementById("first_hatchIN").value,
                'second_hatch':     document.getElementById("second_hatchIN").value,
                'third_hatch':      document.getElementById("third_hatchIN").value,
                'ship_hatch':       document.getElementById("ship_hatchIN").value,

                'totalCargo':       document.getElementById("total_cargoIN").value,
                'first_cargo':      document.getElementById("first_cargoIN").value,
                'second_cargo':     document.getElementById("second_cargoIN").value,
                'third_cargo':      document.getElementById("third_cargoIN").value,
                'ship_cargo':       document.getElementById("ship_cargoIN").value,

                'auto_cargo':       document.getElementById("auto_cargoIN").value,
                'auto_hatch':       document.getElementById("auto_hatchIN").value,
                'first_start':      document.getElementById("first_startIN").value,
                'second_start':     document.getElementById("second_startIN").value,

                'climb':            document.getElementById("climbIN").value,

                'wins':             document.getElementById("winsIN").value,

                'defense_time':     document.getElementById("defense_timeIN").value,

                },
        dataType: "json",
        success: function(data) {
            //console.log(data.content);
            document.getElementById("test").src = "data:image/png;base64," + data.content;
        },
        failure: function (data) {
            console.log("Failed");
        },

    });

}

function toggle(ParentID, call_element, value){
    var children = document.getElementById(ParentID).children;
    for (var i = 0; i < children.length; i++){
        if(children[i].tagName === 'BUTTON')
            children[i].style.opacity = '.5';
        else if (children[i].tagName === 'INPUT')
            children[i].value = value;
    }
    call_element.style.opacity = '1';

    if (ParentID === "GraphToggle") {
        document.getElementById('1').style.display = 'none';
        document.getElementById('2').style.display = 'none';
        document.getElementById('3').style.display = 'none';
        document.getElementById(value.toString()).style.display = 'flex';
        //console.log(value.toString());
    }

}

function select(element) {
    if (document.getElementById(element.id + 'IN').value === 'true'){
        document.getElementById(element.id + 'IN').value = false;
        element.style.opacity = '0.5';
    }
    else {
        document.getElementById(element.id + 'IN').value = true;
        element.style.opacity = '1';
    }

}