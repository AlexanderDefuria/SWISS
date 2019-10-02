function updateImage(){
    $.ajax({
        url: 'update/',
        type: 'get',
        dataType: "json",
        success: function(data) {
            console.log("jh");
        },
        failure: function (data) {
            console.log("Failed");
        },

    });


}