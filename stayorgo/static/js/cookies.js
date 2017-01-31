/**
 * Created on 21/12/2016.
 */
$(load_configuration());

$('#remember_settings').click(function(){
    //console.log("Saving Cookies...");
    save_configuration(90); //save cookies for the season (3 months)
});

$('#clear_cache').click(function(){
    //console.log("Deleting Cookies...");
    save_configuration(0); //delete all cookies
    //load_configuration(); //then 'refresh' the display
});

function setCookie(cname, cvalue, exdays) {
    if (exdays == 0){
        document.cookie = cname + "=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/";
    }else {
        var d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }
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
    $('#weather_station').val(getCookie("weather_station")).trigger('change');
    $('#weather_town').val(getCookie("weather_town")).trigger('change');
    $('#fire_district').val(getCookie("fire_district")).trigger('change');
    $('#fdi_leave_trigger').val(getCookie("fdi_leave_trigger")).trigger('change');
    $('#default_mcarthur_fuel').val(getCookie("default_mcarthur_fuel")).trigger('change');
    $('#default_mcarthur_drought').val(getCookie("default_mcarthur_drought")).trigger('change');
    $('#default_mcarthur_slope').val(getCookie("default_mcarthur_slope")).trigger('change');
    $('#weather_lat').val(getCookie("weather_lat")).trigger('change');
    $('#weather_lon').val(getCookie("weather_lon")).trigger('change');


    // Check boxes are a little different
    //console.log(getCookie('check_town'), getCookie('check_latlon'));
//    if (getCookie('check_town') == 'true'){
//        $('#check_town').attr('checked',true);
//    }else{
//        $('#check_town').attr('checked',false);
//    }
//    if (getCookie('check_latlon') == 'true'){
//        $('#check_latlon').attr('checked',true);
//    }else{
//        $('#check_latlon').attr('checked',false);
//    }


}

function save_configuration(days) {
    //console.log("Saving Cookies...");

    setCookie("weather_station", $('#weather_station').val(), days);
    setCookie("weather_town", $('#weather_town').val(), days);
    setCookie("fire_district", $('#fire_district').val(), days);
    setCookie("fdi_leave_trigger", $('#fdi_leave_trigger').val(), days);
    setCookie("default_mcarthur_fuel", $('#default_mcarthur_fuel').val(), days);
    setCookie("default_mcarthur_drought", $('#default_mcarthur_drought').val(), days);
    setCookie("default_mcarthur_slope", $('#default_mcarthur_slope').val(), days);
    setCookie("weather_lat", $('#weather_lat').val(), days);
    setCookie("weather_lon", $('#weather_lon').val(), days);

    // Check boxes are a little different
//    if ($('#check_town').is(':checked')) {
//        setCookie("check_town", 'true', days);
//    }else {
//        setCookie("check_town", 'false', days);
//    }
//    if ($('#check_latlon').is(':checked')) {
//       setCookie("check_latlon", 'true', days);
//    }else{
//        setCookie("check_latlon", 'false', days);
//    }
}