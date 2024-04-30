// Please see documentation at https://learn.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.

function getBase64Image(img) {
    // Create an empty canvas element
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;

    // Copy the image contents to the canvas
    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);

    // Get the data-URL formatted image
    // Firefox supports PNG and JPEG. You could check img.src to
    // guess the original format, but be aware the using "image/jpg"
    // will re-encode the image.
    var dataURL = canvas.toDataURL("image/png");

    return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
}

var loadFile = function(event) {
	var image = document.getElementById('output');
	image.src = URL.createObjectURL(event.target.files[0]);
};

function downloadImage() {
    var a = document.createElement("a"); //Create <a>
    a.href = "data:image/png;base64," + getBase64Image(document.getElementById("output")); //Image Base64 Goes here
    a.download = "Cool_modified_image.png"; //File name Here
    a.click(); //Downloaded file
}

function editImage(action, params, types) {
    $('#passwordsNoMatchRegister').slideDown();
    $.ajax({
        type: "POST",
        url: "/api/DynamicPhotoEditor/EditImage",
        data: JSON.stringify(
            {
                Base64Blob: getBase64Image(document.getElementById("output")), 
                DynamicAction: action, 
                Parameters:JSON.stringify(params),
                Types: (types == undefined) ? null : types
            }),
        dataType: "json",
        contentType: "application/json",

        success: function (msg) {
            document.getElementById("output").src = "data:image/png;base64," + msg.base64Blob;
            $('#lastException').hide();
        },
        error: function (req, status, error) {
            var error_obj = JSON.parse(req.responseText);
            document.getElementById("lastException").innerText = error_obj.error;
            $('#lastException').fadeIn(500);
        }
    });
}