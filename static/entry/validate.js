function validate(formName, ajax=true) {
    let toSend = {};
    let element;
    let elements = document.forms[formName].getElementsByTagName("input");
    let ignored = ["button", "hidden", "submit", "checkbox"]
	var x = document.getElementById("snackbar");
	var y = document.getElementById("snacktext");

	
    // Go over each input and add them to a list to be verified by server
    for (element in elements)
        if (elements.hasOwnProperty(element)) {
            if (ignored.includes(elements[element].type)) continue;
            if (elements[element].tagName === "INPUT") {
                toSend[elements[element].name] = elements[element].value;
                if (elements[element].type === "number" && elements[element].value === '')
                    toSend[elements[element].name] = 0
            }
        }
    console.log("toSend");
    console.log(toSend);

    if (ajax)
    $.ajax({
        url: 'check/',
        method: 'POST',
		dataType: "json",
        data: toSend,
        success: function(data) {
            let send = true;
            console.log("data");
            console.log(data);
            data = $.parseJSON(data.content);
            console.log(data);
            for (let dataKey in data)
                if (data.hasOwnProperty(dataKey))
                    if (send)
                        send = send !== data[dataKey];
            if (send)
                if (window.confirm("Are You Sure The Data You Entered is Accurate?"))
                    console.log(HTMLFormElement.prototype.submit.call(document.getElementById(formName)));
		    console.log(data);
            let color;
            for (let dataKey in data) {
                if (data.hasOwnProperty(dataKey)) {
                    if (data[dataKey]) {
                        color = '#FF3333'
                    } else {
                        color = '#0F4D8D'
                    }
                    console.log("TRYING TO COLOUR -- " + String(dataKey))
                    let parent = document.getElementById(dataKey);
                    let search = false

                    while (!search) {
                        parent = parent.parentElement;
                        search = (parent.className.includes("formItem"));
                        console.log(parent)
                    }

                    parent.style.backgroundColor = color;
                    x.className = "show";
                    y.innerHTML = "There is a problem with " + dataKey + "!";
                    setTimeout(function () {
                        x.className = x.className.replace("show", "");
                    }, 3000);
                }
            }


        },
        failure: function () {
            console.log("Failed");
        },
    });

    if (!ajax)
        if (window.confirm("Are You Sure You Want To Change Settings?"))
            HTMLFormElement.prototype.submit.call(document.getElementById(formName))

}