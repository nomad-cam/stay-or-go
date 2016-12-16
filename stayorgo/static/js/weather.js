$('#mcarthur_load_weather').click(function(){
  fetch_current_weather();
  //console.log("loading weather data");
});

function fetch_current_weather(){
    //
    //console.log("going");
    //console.log($('#weather_station option:selected').val());
    var error = "    The following errors need to be fixed before continuing: ";
    if ($('#weather_station option:selected').val() == 0){
        error += "<li>No Weather Station has been selected</li>";
        //return;
        $('#custom_error').html("<div class='alert alert-danger alert-dismissible' role='alert' id='alert_error'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>An Error Occured!</strong>" + error + "</div>");
        error = "";
        return;
    }
    var wmo_station_id = $('#weather_station option:selected').val();
    var station_json = "http://www.bom.gov.au/fwo/IDV60801/IDV60801." + wmo_station_id + ".json";
    //console.log(station_json);

    $.ajax({
        dataType: "jsonp",
        jsonp: "onJSONPLoad",
        contentType: 'application/x-www-form-urlencoded',
        type: 'GET',
        url: station_json,
        //data: data,
        //corsDomain: true,
        success: function(data) {
            console.log(data);
           // var items = [];
           //  $.each( data, function( key, val ) {
           //      items.push( "<li id='" + key + "'>" + val + "</li>" );
           //  });
         
           //  $( "<ul/>", {
           //      "class": "my-new-list",
           //      html: items.join( "" )
           //  }).appendTo( "body" ); 
        }
    });

    // $.getJSON(station_json, function(data){
    //     //
    //     var items = [];
    //     $.each( data, function( key, val ) {
    //         items.push( "<li id='" + key + "'>" + val + "</li>" );
    //     });
     
    //     $( "<ul/>", {
    //         "class": "my-new-list",
    //         html: items.join( "" )
    //     }).appendTo( "body" );
    // });



    // if (error.length > 65) {
    //     $('#custom_error').html("<div class='alert alert-danger alert-dismissible' role='alert' id='alert_error'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>An Error Occured!</strong>" + error + "</div>");
    //     //$('.alert').show();
    //     //console.log(error);
    //     error = "";
    //     return;
    // }
};