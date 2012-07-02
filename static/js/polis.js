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

  lookupCoordinates(position.coords.latitude, position.coords.longitude)
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
  $('img.loading').show();
  params = { 'address': address };
  $('#results').load("lookup?" + $.param(params), function() {
    $('img.loading').hide();
    $(this).hide().fadeIn('slow');
  });
}

function lookupCoordinates(lat, lng) {
  $('img.loading').show();
  params = { 'lat': lat, 'lng': lng };
  $('#results').load("lookup?" + $.param(params), function() {
    $('img.loading').hide();
    $(this).hide().fadeIn('slow');
  });
}

$(document).ready(function () {

  $('img.loading').hide();

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
