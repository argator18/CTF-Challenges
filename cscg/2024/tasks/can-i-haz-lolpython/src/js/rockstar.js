function transpile() {

    var data = {"code": document.getElementById("in").value};
    console.log(data);

$.post({
    url: "transpile.php",
    data: JSON.stringify(data)
  }).done(function( data ) {
    var json_data = JSON.parse(data)
    document.getElementById("output").value = json_data["result"];
  });
}