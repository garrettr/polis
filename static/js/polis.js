function geolocate() {
  navigator.geolocation.getCurrentPosition(
      handle_geolocation_result,
      handle_geolocation_error
    );
}

function handle_geolocation_result(position) {
  console.log( 'Lat: ' + position.coords.latitude +
               'Lng: ' + position.coords.longitude
    );

}

function handle_geolocation_error(error) {
  switch(error.code)
  {
    case error.PERMISSION_DENIED:
      console.log("User did not share geolocation data");
      break;

    case error.POSITION_UNAVAILABLE:
      console.log("Could not detect current position");
      break;

    case error.TIMEOUT:
      console.log("retrieving position timed out");
      break;

    default:
      console.log("unknown error");
      break;
  }
}

function lookupAddress(address) {
  params = { 'address': address };
  $('#results').load("lookup?" + $.param(params));
}

function lookupCoordinates(lat, lng) {
}

$(document).ready(function () {

  /* Lookup user's location with the HTML5 geolocation API */
  $("#geolocate").click(geolocate);

  /* Lookup user's location by asking for their address */
  $("form").submit(function (){
    /* copy input values into an object */
    var values = {};
    $.each($(this).serializeArray(), function(i, field) {
      values[field.name] = field.value;
    });
    lookupAddress(values.address);
    return false;
  });

});
