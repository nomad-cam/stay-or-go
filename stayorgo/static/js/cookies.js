/**
 * Created by roddac on 21/12/2016.
 */
$(load_configuration());

$('#remember_settings').click(function(){
    //console.log("Saving Cookies...");
    save_configuration();
});

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}


function load_configuration(){
    //
    //console.log("Loading Cookies...");
    //console.log(getCookie("weather_station"));
    //console.log(getCookie("weather_town"));
    //console.log(getCookie("fire_district"));
    //console.log(getCookie("fdi_leave_trigger"));
    //console.log(getCookie("default_mcarthur_fuel"));
    //console.log(getCookie("default_mcarthur_drought"));
    //console.log(getCookie("default_mcarthur_slope"));

    $('#weather_station').val(getCookie("weather_station")).trigger('change');
    $('#weather_town').val(getCookie("weather_town")).trigger('change');
    $('#fire_district').val(getCookie("fire_district")).trigger('change');
    $('#fdi_leave_trigger').val(getCookie("fdi_leave_trigger")).trigger('change');
    $('#default_mcarthur_fuel').val(getCookie("default_mcarthur_fuel")).trigger('change');
    $('#default_mcarthur_drought').val(getCookie("default_mcarthur_drought")).trigger('change');
    $('#default_mcarthur_slope').val(getCookie("default_mcarthur_slope")).trigger('change');

}

function save_configuration(){
    // cookie time to 30 days...
    //console.log("Saving Cookies...");
    setCookie("weather_station",$('#weather_station').val(),30);
    setCookie("weather_town",$('#weather_town').val(),30);
    setCookie("fire_district",$('#fire_district').val(),30);
    setCookie("fdi_leave_trigger",$('#fdi_leave_trigger').val(),30);
    setCookie("default_mcarthur_fuel",$('#default_mcarthur_fuel').val(),30);
    //console.log("Saving fuel load: "+$('#default_mcarthur_fuel').val());
    setCookie("default_mcarthur_drought",$('#default_mcarthur_drought').val(),30);
    setCookie("default_mcarthur_slope",$('#default_mcarthur_slope').val(),30);
}