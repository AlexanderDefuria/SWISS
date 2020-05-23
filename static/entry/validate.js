function validate(formName) {
    let toSend = {};
    let element;
    let elements = document.forms[formName].getElementsByTagName("input");
    let ignored = ["button", "hidden", "submit", "checkbox", "radio"]

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
    console.log(toSend)

    $.ajax({
        url: 'check/',
        method: 'POST',
		dataType: "json",
        data: toSend,
        success: function(data) {
            let send = true;
            data = $.parseJSON(data.content);
            console.log(data)
            for (let dataKey in data)
                if (data.hasOwnProperty(dataKey))
                    if (send)
                        send = send !== data[dataKey];
            if (send) console.log(HTMLFormElement.prototype.submit.call(document.getElementById(formName)));
		    console.log(data);
            for (let dataKey in data){
		        if (data.hasOwnProperty(dataKey))
		            if (data[dataKey]) {
		                console.log("TRYING TO REDLINE -- " + String(dataKey))
		                let parent = document.getElementById(dataKey);
		                let search = false

		                while (!search) {
		                    parent = parent.parentElement;
                            search = (parent.className.includes("formItem"));
                            console.log(parent)
                        }


		                parent.style.backgroundColor = 'lightcoral';
		                window.alert("There is an issue with the data given for " + dataKey)
                    }
            }

        },
        failure: function () {
            console.log("Failed");

        },
    });

        HTMLFormElement.prototype.submit.call(document.getElementById(formName))

}