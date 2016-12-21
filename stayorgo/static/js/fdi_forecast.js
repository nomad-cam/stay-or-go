/**
 * Created by roddac on 21/12/2016.
 */

function tonum(obj)
{
  return parseFloat(obj);
}

$("#forecast_fdi_calculate").click(function(){
    console.log("Clicked Calculate!")
    check_fdi_input();
});


function check_fdi_input(){
    //
    //
    error = "";
    if($('#weather_town').val().length == 0) {
        error += "<li>No value entered for Nearest Town/Suburb</li>"; //
    }
    if($('#default_mcarthur_fuel').val().length == 0) {
        error += "<li>No value entered for Default Fuel Load</li>"; //
    }
    if($('#default_mcarthur_drought').val().length == 0) {
        error += "<li>No value entered for Default Drought Factor</li>"; //
    }
    if($('#default_mcarthur_slope').val().length == 0) {
        error += "<li>No value entered for Default Ground Slope</li>"; //
    }

    if(error.length > 0){
        generate_error(error);
    }else{
        calc_fdi_forecast();
    }
}


function mcarthur_calc_fdi_forecast(a,b,c,d,f,h) {
    // Originally created by Pat Barling http://www.firebreak.com.au/forest-5.html
    //console.log("entering calc_fdi");
    //var a = tonum($('#mcarthur_slope').val());//slope
    //var b = tonum($('#mcarthur_temp').val());//temperature
    //var c = tonum($('#mcarthur_humid').val());//rel humidity
    //var d = tonum($('#mcarthur_wind').val());//wind speed
    //var f = tonum($('#mcarthur_fuel').val());//fuel load
    //var h = tonum($('#mcarthur_drought').val());//drought factor
    //console.log("imported values");
    //console.log(a,b,c,d,f,h);
    var k = 2 * (Math.exp((.987 * Math.log(h + 0.001)) - .45 - (.0345 * c) + (.0338 * b) + (.0234 * d)));//forest mk5
    //var j = (0.0012 * k * f);
    //var l = (13 * j) + (0.24 * f) - 2;//flame height - forest
    //var z = (j * (4.17 - (0.033 * f))) - 0.36;//Distance of spotting from flame front
    //var v = j * (Math.exp(0.069 * a));//Rate of spread
    //console.log(k,j,l,z,v);
    {
        var img = "/static/img/fdr_null_new.png";
        if (Math.round(k) == 0) {
            var s = (" NIL");
        }
        else if (k < 12) {
            var s = (Math.round(k) + " (LOW - MODERATE)");
            var img = "/static/img/fdr_low_new.png";
        }
        else if (k < 24) {
            var s = (Math.round(k) + " (HIGH)");
            var img = "/static/img/fdr_high_new.png";
        }
        else if (k < 50) {
            var s = (Math.round(k) + " (VERY HIGH)");
            var img = "/static/img/fdr_veryhigh_new.png";
        }
        else if (k < 75) {
            var s = (Math.round(k) + " (SEVERE)");
            var img = "/static/img/fdr_severe_new.png";
        }
        else if (k < 100) {
            var s = (Math.round(k) + " (EXTREME)");
            var img = "/static/img/fdr_extreme_new.png";
        }
        else if (k > 100) {
            var s = (Math.round(k) + " (CODE RED)");
            var img = "/static/img/fdr_codered_new.png";
        }
    }
    return s; // return FDI + text description
}


function calc_fdi_forecast(){
    //
    // Clear Previous Results
    $('#display_forecast_fdi_custom').html("");


    var town = $('#weather_town').val();
    var fuel = tonum($('#default_mcarthur_fuel').val());
    var drought = tonum($('#default_mcarthur_drought').val());
    var slope = tonum($('#default_mcarthur_slope').val());

    $.ajax({
        dataType: 'json',
        type: 'POST',
        url: '/api/wu/forecast/'+town,
        success: function(data){
            //
            for(var i = 0; i< data.length; i++){
                temp = tonum(data[i]['temp']['metric']);
                humidity = tonum(data[i]['humidity']);
                wind_spd_kmh = tonum(data[i]['wspd']['metric']);
                //console.log(temp,humidity,wind_spd_kmh,fuel,drought,slope);
                fdi = mcarthur_calc_fdi_forecast(slope,temp,humidity,wind_spd_kmh,fuel,drought);
                final_date = data[i]['FCTTIME']['mday_padded'] + " " + data[i]['FCTTIME']['month_name'] + " - " +
                             data[i]['FCTTIME']['civil'];

                var panel_string = "<div class='panel-body text-center'>";
                if(fdi.indexOf("(LOW") > 0){
                    panel_string = "<div class='panel-body low-bg text-center'>"
                }
                if(fdi.indexOf("(HIGH") > 0){
                    panel_string = "<div class='panel-body high-bg text-center'>"
                }
                if(fdi.indexOf("(VERY HIGH") > 0){
                    panel_string = "<div class='panel-body veryhigh-bg text-center'>"
                }
                if(fdi.indexOf("(SEVERE") > 0){
                    panel_string = "<div class='panel-body severe-bg text-center'>"
                }
                if(fdi.indexOf("(EXTREME") > 0){
                    panel_string = "<div class='panel-body extreme-bg text-center'>"
                }
                if(fdi.indexOf("(CODE RED") > 0){
                    panel_string = "<div class='panel-body codered-bg text-center'>"
                }


                var forecast = "<div class='panel panel-default'><div class='panel-heading'><b>"+final_date+"</b></div>" +
                        panel_string + fdi +"</div></div>";
                //console.log(forecast);

                $('#display_forecast_fdi_custom').append(forecast);
            }

        }
    });

}


function generate_error(error){
    $('#flash').html("<div class='alert alert-danger alert-dismissible' role='alert' id='alert_error'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>An Error Occured!</strong>" + error + "</div>");
}

