/**
 * Created on 30/12/2018.
 */

function tonum(obj)
{
  return parseFloat(obj);
}

// $(document).ready() run when the page has loaded
$(calc_fdi_forecast10());

$('#weather_town').change(function(){
    calc_fdi_forecast10();
});

$('#load_forecast10').click(function(){
    $('#forecast10_display').html("");
    $('#forecast10_display_small').html("");
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

    var source = $('#weather_server').val();
    var burb = $('#weather_town').val();
    var town = $('#weather_lat').val() + ',' + $('#weather_lon').val();
    // var fuel = tonum($('#default_mcarthur_fuel').val());
    var drought = tonum($('#default_mcarthur_drought').val());
    // var slope = tonum($('#default_mcarthur_slope').val());
    var leave = $('#fdi_leave_trigger option:selected').text().toUpperCase();
    // console.log(leave);
    var trigger_once = false;
    //console.log(trigger_once);

    var months = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'];

    $.ajax({
        dataType: 'json',
        type: 'POST',
        url: '/api/wx/forecast/'+source+'/'+town,
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
                date = new Date(data[i]['datetime']);
                temp = tonum(data[i]['maxTemp']);
                humidity = tonum(data[i]['minRH']);
                wind_spd_kmh = tonum(data[i]['avgWindSpd']);
                //console.log(temp,humidity,wind_spd_kmh,fuel,drought,slope);
                fdi = mcarthur_calc_fdi_forecast(temp,humidity,wind_spd_kmh,drought);
                // final_date_time = data[i]['FCTTIME']['mday_padded'] + " " + data[i]['FCTTIME']['month_name'] + " - " +
                //              data[i]['FCTTIME']['civil'];
                // 01 January - 11:00 AM
                final_date_time = ((date.getDate() < 10)?'0':'') + date.getDate() + " " + months[date.getMonth()] + " - " +
                    (date.getHours() % 12 || 12) + ":" + ('00' + date.getMinutes()).slice(-2) + " " + ((date.getHours() >= 12)?"PM":"AM");
                // console.log(final_date_time);

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
                    // console.log(fdi,"("+leave);
                    if (fdi.indexOf("(" + leave) > 0) {
                        if((i-1) < 0){
                            // if leave time is now; unable to leave earlier
                            leave_date_time = ((date.getDate() < 10)?'0':'') + date.getDate() + " " + months[date.getMonth()] + " - " +
                                                (date.getHours() % 12 || 12) + ":" + ('00' + date.getMinutes()).slice(-2) + " " + ((date.getHours() >= 12)?"PM":"AM");
                        }else {
                            // else leave time an hour prior to severity condition
                            previous_date = new Date(data[i-1]['datetime']);
                            leave_date_time = ((previous_date.getDate() < 10)?'0':'') + previous_date.getDate() + " " + months[previous_date.getMonth()] + " - " +
                                                (previous_date.getHours() % 12 || 12) + ":" + ('00' + previous_date.getMinutes()).slice(-2) + " " + ((previous_date.getHours() >= 12)?"PM":"AM");
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
    // Clear Previous Results
    $('#forecast10_display').html("");
    $('#forecast10_display_small').html("");
    $('#forecast10_title').html("Undefined");

    var source = $('#weather_server').val();
    var town = $('#weather_lat').val() + ',' + $('#weather_lon').val();
    var burb = $('#weather_town').val();
    if (burb == ""){
        $('#forecast10_title').html("Undefined");
        return;
    }

    var dow = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    var mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    var drought = tonum($('#default_mcarthur_drought').val());

    $.ajax({
        dataType: 'json',
        type: 'POST',
        url: '/api/wx/forecast10/'+source+'/'+town,
        success: function(data){
            for(var i = 0; i< data.length; i++){
                date = new Date(data[i]['datetime']);
                temp = tonum(data[i]['maxTemp']);
                humidity = tonum(data[i]['minRH']);
                wind_spd_kmh = tonum(data[i]['avgWindSpd']);
                // console.log(temp,humidity,wind_spd_kmh,drought);
                fdi = mcarthur_calc_fdi_forecast(temp,humidity,wind_spd_kmh,drought);

                // check for errors in input data, mainly if data == 0;
                var img_str = '';
                if((temp == 0)||(humidity == 0)||(wind_spd_kmh == 0)){
                    img_str = "<image src='/static/img/error_character.png' style='width: 25px; height: 25px'>";
                }
                $('#forecast10_title').html(img_str + " " + burb + " " + img_str);

                // final_date = data[i]['date']['weekday_short'] + ", " + data[i]['date']['day'] + " " +
                //              data[i]['date']['monthname_short'];
                final_date = dow[date.getDay()] + ", " + date.getDate() + ", " + mon[date.getMonth()];
                // final_date_small = data[i]['date']['day'] + " " + data[i]['date']['monthname_short'] + " " + data[i]['date']['year'];
                final_date_small = date.getDate() + " " + mon[date.getMonth()] + " " + date.getFullYear();

                var input = "Temp: "+temp+"&deg;C; Wind:"+wind_spd_kmh+"km/h; Humidity:"+humidity+"%";
                var input_small = "Temp:  "+temp+"&deg;C<br>Wind:  "+wind_spd_kmh+"km/h<br>Humidity:  "+humidity+"%";

                var panel_string = "<div class='panel-body panel-content-small panel-fixed-height text-center' title='"+input+"'>";
                var panel_string_small = "<button class='btn btn-sq-xs' data-toggle='popover' data-placement='top' " +
                                         "title='Date: "+final_date_small+"' data-content='<b>FDI: </b>NaN<br><b>FDR: </b>NaN<br>" +
                                         input_small + "'></button>";

                fdi_split = fdi.split('(')[0].split(' ')[0];

                if(fdi.indexOf("(LOW") > 0){
                    panel_string = "<div class='panel-body panel-content-small panel-fixed-height low-bg text-center' title='"+input+"'>";
                    panel_string_small = "<button class='btn btn-sq-xs low-bg' data-toggle='popover' data-placement='top' " +
                                         "title='"+final_date_small+"' data-content='<b>FDI: </b>"+fdi_split+"<br><b>FDR: </b>LOW-MODERATE<br>" +
                                         input_small + "'></button>";
                }
                if(fdi.indexOf("(HIGH") > 0){
                    panel_string = "<div class='panel-body panel-content-small panel-fixed-height high-bg text-center' title='"+input+"'>";
                    panel_string_small = "<button class='btn btn-sq-xs high-bg' data-toggle='popover' data-placement='top' " +
                                         "title='"+final_date_small+"' data-content='<b>FDI: </b>"+fdi_split+"<br><b>FDR: </b>HIGH<br>" +
                                         input_small + "'></button>";
                }
                if(fdi.indexOf("(VERY HIGH") > 0){
                    panel_string = "<div class='panel-body panel-content-small panel-fixed-height veryhigh-bg text-center' title='"+input+"'>";
                    panel_string_small = "<button class='btn btn-sq-xs veryhigh-bg' data-toggle='popover' data-placement='top' " +
                                         "title='"+final_date_small+"' data-content='<b>FDI: </b>"+fdi_split+"<br><b>FDR: </b>VERY HIGH<br>" +
                                         input_small + "'></button>";
                }
                if(fdi.indexOf("(SEVERE") > 0){
                    panel_string = "<div class='panel-body panel-content-small panel-fixed-height severe-bg text-center' title='"+input+"'>";
                    panel_string_small = "<button class='btn btn-sq-xs severe-bg' data-toggle='popover' data-placement='top' " +
                                         "title='"+final_date_small+"' data-content='<b>FDI: </b>"+fdi_split+"<br><b>FDR: </b>SEVERE<br>" +
                                         input_small + "'></button>";
                }
                if(fdi.indexOf("(EXTREME") > 0){
                    panel_string = "<div class='panel-body panel-content-small panel-fixed-height extreme-bg text-center' title='"+input+"'>";
                    panel_string_small = "<button class='btn btn-sq-xs extreme-bg' data-toggle='popover' data-placement='top' " +
                                         "title='"+final_date_small+"' data-content='<b>FDI: </b>"+fdi_split+"<br><b>FDR: </b>EXTREME<br>" +
                                         input_small + "'></button>";
                }
                if(fdi.indexOf("(CODE RED") > 0){
                    panel_string = "<div class='panel-body panel-content-small panel-fixed-height codered-bg text-center' title='"+input+"'>";
                    panel_string_small = "<button class='btn btn-sq-xs codered-bg' data-toggle='popover' data-placement='top' " +
                                         "title='"+final_date_small+"' data-content='<b>FDI: </b>"+fdi_split+"<br><b>FDR: </b>CODE-RED<br>" +
                                         input_small + "'></button>";
                }

                var forecast10 = "<div class='col-md-1'><div class='panel panel-default panel-custom-margin'><div class='panel-heading panel-content-small'>" +
                               "<b><div class='text-center'>" + final_date+"</div></b>" +
                               "</div>" + panel_string + fdi +"</div></div></div>";

                $('#forecast10_display').append(forecast10);
                $('#forecast10_display_small').append(panel_string_small);
            }
        }
    });
    // seemed to not load the popovers after loading dynamic content, so repeated at end seems to sort it out...
    $('[data-toggle="popover"]').popover({
        html: true
    });
}


function generate_error(error){
    $('#flash').html("<div class='alert alert-danger alert-dismissible' role='alert' id='alert_error'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>An Error Occured!</strong>" + error + "</div>");
}

function generate_warning(error){
    $('#flash').html("<div class='alert alert-info alert-dismissible' role='alert' id='alert_info'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>Important Information!</strong>" + error + "</div>");
}

