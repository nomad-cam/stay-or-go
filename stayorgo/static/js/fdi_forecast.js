/**
 * Created on 21/12/2016.
 */

function tonum(obj)
{
  return parseFloat(obj);
}

// $(document).ready() run when the page has loaded
$(calc_fdi_forecast10())

$('#weather_town').change(function(){
    calc_fdi_forecast10();
});

$('#load_forecast10').click(function(){
    $('#forecast10_display').html("");
    $('#forecast10_title').html("Undefined");
    calc_fdi_forecast10();
});

$("#forecast_fdi_calculate").click(function(){
    //console.log("Clicked Calculate!")
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


function mcarthur_calc_fdi_forecast(b,c,d,h) {
    // Originally created by Pat Barling http://www.firebreak.com.au/forest-5.html
    var k = 2 * (Math.exp((.987 * Math.log(h + 0.001)) - .45 - (.0345 * c) + (.0338 * b) + (.0234 * d)));//forest mk5

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

    var burb = $('#weather_town').val();
    var town = $('#weather_lat').val() + ',' + $('#weather_lon').val();
    // var fuel = tonum($('#default_mcarthur_fuel').val());
    var drought = tonum($('#default_mcarthur_drought').val());
    // var slope = tonum($('#default_mcarthur_slope').val());
    var leave = $('#fdi_leave_trigger option:selected').text().toUpperCase();
    //console.log(leave);
    var trigger_once = false;
    //console.log(trigger_once);

    $.ajax({
        dataType: 'json',
        type: 'POST',
        url: '/api/wu/forecast/'+town,
        success: function(data){
            //
            current_date = new Date()
            atm = '<p class="text-center"><small>Calculated: '
                         + ((current_date.getDate() < 10)?'0':'') + current_date.getDate() + '/'
                         + ((current_date.getMonth() < 10)?'0':'') + (current_date.getMonth()+1) + '/'
                         + current_date.getFullYear() + ' '
                         + ((current_date.getHours() < 10)?'0':'') + current_date.getHours() + ':'
                         + ((current_date.getMinutes() < 10)?'0':'') + current_date.getMinutes() + ':'
                         + ((current_date.getSeconds() < 10)?'0':'') + current_date.getSeconds()
                         + '</small><br><h3 class="text-center">Forecast for '+ burb +'</h3></p>';
            $('#display_forecast_fdi_custom').html(atm);
            for(var i = 0; i< data.length; i++){
                temp = tonum(data[i]['temp']['metric']);
                humidity = tonum(data[i]['humidity']);
                wind_spd_kmh = tonum(data[i]['wspd']['metric']);
                //console.log(temp,humidity,wind_spd_kmh,fuel,drought,slope);
                fdi = mcarthur_calc_fdi_forecast(temp,humidity,wind_spd_kmh,drought);
                final_date_time = data[i]['FCTTIME']['mday_padded'] + " " + data[i]['FCTTIME']['month_name'] + " - " +
                             data[i]['FCTTIME']['civil'];

                var input = "Temp: "+temp+"&deg;C; Wind:"+wind_spd_kmh+"km/h; Humidity:"+humidity+"%";

                var panel_string = "<div class='panel-body panel-content-small text-center' title='"+input+"'>";
                if(fdi.indexOf("(LOW") > 0){
                    panel_string = "<div class='panel-body panel-content-small low-bg text-center' title='"+input+"'>"
                }
                if(fdi.indexOf("(HIGH") > 0){
                    panel_string = "<div class='panel-body panel-content-small high-bg text-center' title='"+input+"'>"
                }
                if(fdi.indexOf("(VERY HIGH") > 0){
                    panel_string = "<div class='panel-body panel-content-small veryhigh-bg text-center' title='"+input+"'>"
                }
                if(fdi.indexOf("(SEVERE") > 0){
                    panel_string = "<div class='panel-body panel-content-small severe-bg text-center' title='"+input+"'>"
                }
                if(fdi.indexOf("(EXTREME") > 0){
                    panel_string = "<div class='panel-body panel-content-small extreme-bg text-center' title='"+input+"'>"
                }
                if(fdi.indexOf("(CODE RED") > 0){
                    panel_string = "<div class='panel-body panel-content-small codered-bg text-center' title='"+input+"'>"
                }

                // compare the fdi text to the users leave trigger and display a message if required

                if(trigger_once == false) {
                    //console.log(trigger_once);
                    //console.log(fdi,"("+leave);
                    if (fdi.indexOf("(" + leave) > 0) {
                        if((i-1) < 0){
                            leave_date_time = data[i]['FCTTIME']['mday_padded'] + " " + data[i]['FCTTIME']['month_name'] + " - " +
                                data[i]['FCTTIME']['civil'];
                        }else {
                            leave_date_time = data[i - 1]['FCTTIME']['mday_padded'] + " " + data[i - 1]['FCTTIME']['month_name'] + " - " +
                                data[i - 1]['FCTTIME']['civil'];
                        }
                        generate_warning("<br>Your leave early trigger has been met. Leave before <b><u>" + leave_date_time + "</u></b><br>" +
                                       "Continue to monitor your local weather conditions as forecast data may not accurately reflect current observed conditions.");
                        trigger_once = true;
                    }

                }

                var forecast = "<div class='panel panel-default panel-custom-margin'><div class='panel-heading panel-content-small'><b>"+final_date_time+"</b></div>" +
                        panel_string + fdi +"</div></div>";
                //console.log(forecast);

                $('#display_forecast_fdi_custom').append(forecast);
            }

        }
    });

}


function calc_fdi_forecast10(){
//    console.log('Calculating 10 Day forecast');
    // Clear Previous Results
    $('#forecast10_display').html("");
    $('#forecast10_title').html("Undefined");

    var town = $('#weather_lat').val() + ',' + $('#weather_lon').val();
    var burb = $('#weather_town').val();
    if (burb == ""){
        $('#forecast10_title').html("Undefined");
        return;
    }


    var drought = tonum($('#default_mcarthur_drought').val());

    $.ajax({
        dataType: 'json',
        type: 'POST',
        url: '/api/wu/forecast10/'+town,
        success: function(data){
//            console.log(data);
            for(var i = 0; i< data.length; i++){
//                console.log(data[i]);
                temp = tonum(data[i]['high']['celsius']);
                humidity = tonum(data[i]['minhumidity']);
                wind_spd_kmh = tonum(data[i]['avewind']['kph']);
                //console.log(temp,humidity,wind_spd_kmh,fuel,drought,slope);
                fdi = mcarthur_calc_fdi_forecast(temp,humidity,wind_spd_kmh,drought);
//                console.log(fdi);
//                $('#forecast10_display').append("<div class='col-sm-1'>")

                $('#forecast10_title').html(burb);

                final_date_time = data[i]['date']['weekday_short'] + ", " + data[i]['date']['day'] + " " +
                             data[i]['date']['monthname_short'];

                var input = "Temp: "+temp+"&deg;C; Wind:"+wind_spd_kmh+"km/h; Humidity:"+humidity+"%";

                var panel_string = "<div class='panel-body panel-content-small panel-fixed-height text-center' title='"+input+"'>";
                if(fdi.indexOf("(LOW") > 0){
                    panel_string = "<div class='panel-body panel-content-small panel-fixed-height low-bg text-center' title='"+input+"'>"
                }
                if(fdi.indexOf("(HIGH") > 0){
                    panel_string = "<div class='panel-body panel-content-small panel-fixed-height high-bg text-center' title='"+input+"'>"
                }
                if(fdi.indexOf("(VERY HIGH") > 0){
                    panel_string = "<div class='panel-body panel-content-small panel-fixed-height veryhigh-bg text-center' title='"+input+"'>"
                }
                if(fdi.indexOf("(SEVERE") > 0){
                    panel_string = "<div class='panel-body panel-content-small panel-fixed-height severe-bg text-center' title='"+input+"'>"
                }
                if(fdi.indexOf("(EXTREME") > 0){
                    panel_string = "<div class='panel-body panel-content-small panel-fixed-height extreme-bg text-center' title='"+input+"'>"
                }
                if(fdi.indexOf("(CODE RED") > 0){
                    panel_string = "<div class='panel-body panel-content-small panel-fixed-height codered-bg text-center' title='"+input+"'>"
                }

                var forecast10 = "<div class='col-md-1'><div class='panel panel-default panel-custom-margin'><div class='panel-heading panel-content-small'>" +
                               "<b><div class='text-center'>" + final_date_time+"</div></b>" +
                               "</div>" + panel_string + fdi +"</div></div></div>";

                $('#forecast10_display').append(forecast10);
            }
        }
    });
}


function generate_error(error){
    $('#flash').html("<div class='alert alert-danger alert-dismissible' role='alert' id='alert_error'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>An Error Occured!</strong>" + error + "</div>");
}

function generate_warning(error){
    $('#flash').html("<div class='alert alert-info alert-dismissible' role='alert' id='alert_info'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>Important Information!</strong>" + error + "</div>");
}

