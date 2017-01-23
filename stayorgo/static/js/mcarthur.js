function tonum(obj)
{
  return parseFloat(obj);
}

$('#mcarthur_calculate').click(function(){
  //console.log("calculating mcarthur mk5");
  mcarthur_check_input();
});

$('#mcarthur_load_weather').click(function () {
    mcarthur_load_current_weather();
});

$('#mcarthur_reset').click(function(){
  //
  $('#mcarthur_humid').val("");
  $('#mcarthur_temp').val("");
  $('#mcarthur_wind').val("");
  $('#mcarthur_fuel').val("");
  $('#mcarthur_drought').val("");
  $('#mcarthur_slope').val("");

  var img = "/static/img/fdr_null_new.png";
  $('#mcarthur_fdr').attr('src', img);
  $('#mcarthur_result').html("");
});

$('#fuel_load_calculate').click(function(){
  //console.log("calculating mcarthur mk5");
  fuel_load_calculate();
});

function fuel_load_calculate()
{
  var surface = tonum($('#surface_fuel').val());
  var elevated = tonum($('#elevated_fuel').val());
  var bark = tonum($('#bark_fuel').val());
  var near = tonum($('#near_surface_fuel').val());
  // console.log(surface,elevated,bark,near);
  var result = surface + elevated + bark + near;
  $('#fuel_load_result').html("<div style='padding-left: 15px'><h4>  Result: "+ result + " t/ha</h4></div>");
}

function generate_error(error){
    $('#flash').html("<div class='alert alert-danger alert-dismissible' role='alert' id='alert_error'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>An Error Occured!</strong>" + error + "</div>");
}


function mcarthur_check_input()
{
  //console.log('calculating...');
  var error = "    The following errors need to be fixed before continuing: ";
  if($('#mcarthur_temp').val().length == 0) {
    error += "<li>No value entered for Temperature</li>"; // temperature between 0 and 45 degrees
  }
  if($('#mcarthur_humid').val().length == 0) {
    error += "<li>No value entered for Humidity</li>"; // humidity between 0 and 100%
  }
  if($('#mcarthur_wind').val().length == 0) {
    error += "<li>No value entered for Wind Speed</li>"; // windspeed between 0 and 70kmh
  }
  if($('#mcarthur_fuel').val().length == 0) {
    error += "<li>No value entered for Fuel Load</li>"; //fuel load between 1 and 25 tonne/hectare
  }
  if($('#mcarthur_drought').val().length == 0) {
    error += "<li>No value entered for Drought Factor</li>"; // drought factor between 1 and 10
  }
  if($('#mcarthur_slope').val().length == 0) {
    error += "<li>No value entered for Slope</li>"; // slope between 0 and 90 degrees
  }
  //calc_fdi();
  if (error.length > 65) {
    generate_error(error);
    //$('#flash').html("<div class='alert alert-danger alert-dismissible' role='alert' id='alert_error'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>An Error Occured!</strong>" + error + "</div>");
    //$('.alert').show();
    //console.log(error);
    error = "";
    //return;
  } else {
    mcarthur_calc_fdi();
  }

}

function mcarthur_calc_fdi()
{
  // Originally created by Pat Barling http://www.firebreak.com.au/forest-5.html
  //console.log("entering calc_fdi");
  var a=tonum($('#mcarthur_slope').val());//slope
  var b=tonum($('#mcarthur_temp').val());//temperature
  var c=tonum($('#mcarthur_humid').val());//rel humidity
  var d=tonum($('#mcarthur_wind').val());//wind speed
  var f=tonum($('#mcarthur_fuel').val());//fuel load
  var h=tonum($('#mcarthur_drought').val());//drought factor
  //console.log("imported values");
  //console.log(a,b,c,d,f,h);
  var k=2*(Math.exp((.987*Math.log(h+0.001))-.45-(.0345*c)+(.0338*b)+(.0234*d)));//forest mk5
  var j=(0.0012*k*f);
  var l=(13*j)+(0.24*f)-2;//flame height - forest
  var z=(j*(4.17-(0.033*f)))-0.36;//Distance of spotting from flame front
  var v=j*(Math.exp(0.069*a));//Rate of spread
  //console.log(k,j,l,z,v);
    {
      var img = "/static/img/fdr_null_new.png";
      if (Math.round(k) == 0) {
        var s = (" NIL");
      }
      else if  (k<12) {
        var s = (Math.round(k) + " LOW - MODERATE");
        var img = "/static/img/fdr_low_new.png";
      }
      else if  (k<24) {
        var s = (Math.round(k) + " HIGH");
        var img = "/static/img/fdr_high_new.png";
      }
      else if  (k<50) {
        var s = (Math.round(k) + " VERY HIGH");
        var img = "/static/img/fdr_veryhigh_new.png";
      }
      else if  (k<75) {
        var s = (Math.round(k) + " SEVERE");
        var img = "/static/img/fdr_severe_new.png";
      }
      else if  (k<100) {
        var s = (Math.round(k) + " EXTREME");
        var img = "/static/img/fdr_extreme_new.png";
      }
      else if (k>100) {
        var s = (Math.round(k) + " CODE RED");
        var img = "/static/img/fdr_codered_new.png";
      }
    }

    {
      if (l<0)
        var m = 0;

      else if  (l>0)
       var m =((Math.round(l*100))/100 + " m");
    }

    {
      if (z<0)
        var y = 0;

      else if  (z>0)
       var y =((Math.round(z*100))/100 + " km");
    }

    {
      if (v<0)
        var u = 0;

      else if  (v>0)
       var u =((Math.round(v*100))/100 + " km/hr");
    }
  {

  // console.log(s);
  $('#mcarthur_fdr').attr('src', img);
  $('#mcarthur_result').html("<h2>Current FDI:</h2> " + s + "<br><h4>Flame Height:</h4> " + m + "<br><h4>Spotting Distance:</h4> " + y + "<br><h4>Rate of Spread</h4> " + u );
  //form.outputbox3.value=s;//forest mk5
  //form.outputbox5.value=m;//flame height - forests
  //form.outputbox6.value=y;//spotting distance - forests
  //form.outputbox7.value=u;//rate of forward spread on sloping ground  - forests
  }

}

function mcarthur_load_current_weather() {
    var station_id = $('#weather_station option:selected').val();

    if (station_id == 0){
        generate_error("<li>No Weather Station has been selected</li>");
        return;
    }

    $.ajax({
        dataType: 'json',
        type: 'POST',
        url: '/api/wx/current/' + station_id,
        success: function(data){
            //
            //console.log(data);
            $('#mcarthur_temp').val(data['air_temperature']);
            $('#mcarthur_humid').val(data['rel-humidity']);
            $('#mcarthur_wind').val(data['wind_spd_kmh']);
        }
    });

}