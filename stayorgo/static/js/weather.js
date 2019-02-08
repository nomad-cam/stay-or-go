//$(document).ready();
$(load_station_list());
//

$('#forecast_fdi').click(function () {
    fetch_fdi_forecast();
});

$('#fire_district').change(function(){
    //console.log("change in district detected!");
    fetch_fdi_forecast();
});

$('#weather_server').change(function () {
    update_weather_attribution();
});

function load_station_list(){
    $.ajax({
        dataType: 'json',
        type: 'POST',
        url: '/api/wx/station/ALL',
        success: function(data){
            //
            //console.log(data[0]["name"]);
            var station_load = getCookie("weather_station");
            //console.log(station_load);

            var option = "";
            for (var j = 0; j < data.length; j++){
                if (data[j]["bom-id"] == station_load){
                    option += "<option value='" + data[j]["bom-id"] + "' selected>" + data[j]["name"] + "</option>";
                }else {
                    option += "<option value='" + data[j]["bom-id"] + "'>" + data[j]["name"] + "</option>";
                }
            }
            $('#weather_station').append(option);
        }
    });
    // Load the default cookie based value if available
    // console.log("loading default weather station");
    // $('#weather_station').val(getCookie("weather_station"));
}


function fetch_fdi_forecast(){
    //
    var district_check = $('#fire_district option:selected').val();

    if (district_check == '0'){
        generate_error("<li>No Fire District has been selected</li>");
        return;
    }

    var district = $('#fire_district option:selected').text();
    var fdr;
    var tfb;
    //console.log(district);

    //var FEED_URL = "http://www.cfa.vic.gov.au/restrictions/tfbfdrforecast_rss.xml";
    //specify district rather than fetching all the data
    var FEED_FDR_URL = "/api/fx/forecast/fdr/"+district;
    var FEED_TFB_URL = "/api/fx/forecast/tfb/"+district;
    //console.log(FEED_FDR_URL,FEED_TFB_URL);
    $.when(
        $.get(FEED_FDR_URL, function(fdr_data){
            fdr = fdr_data;
        }),
        $.get(FEED_TFB_URL, function(tfb_data){
            tfb = tfb_data;
        })
    ).then(function(){
        // console.log(fdr,tfb);
        $("#display_forecast_fdi_official").html("<p class='text-center'><small>Issued: " + tfb['tfb'][0].fileDate + "</small><br><h3 class='text-center'>"+tfb['tfb'][0].district+" Forecast District</h3></p>");
        for(var h = 0; h < fdr['fdr'].length; h++){
            //console.log(h,tfb['tfb'].length);
            //Check for a declared TFB otherwise default to No TFB
            var tfb_decl_str = "<div class='text-center'>TFB? "+ tfb['tfb'][h].status +"</div>";
            //console.log(tfb_decl[1].indexOf("Yes"));
            if (tfb['tfb'][h].statusShort == 'Y'){
                console.log('TFB Status Active');
                tfb_decl_str = "<p class='text-center'><img src='/static/img/tfb_icon.gif'> TFB? "+ tfb['tfb'][h].status +"</p>";
            }

            //console.log(fdi_decl[1]);
            // determine which image to display
            var img = "/static/img/fdr_null_new.png";
            var img_alt = "no fire danger rating";

            if(fdr['fdr'][h].status == "LOW-MODERATE"){
                var img = "/static/img/fdr_low_new.png";
                var img_alt = "Low moderate fire danger rating";
            }
            if(fdr['fdr'][h].status == "HIGH"){
                var img = "/static/img/fdr_high_new.png";
                var img_alt = "High fire danger rating";
            }
            if(fdr['fdr'][h].status == "VERY HIGH"){
                var img = "/static/img/fdr_veryhigh_new.png";
                var img_alt = "Very High fire danger rating";
            }
            if(fdr['fdr'][h].status == "SEVERE"){
                var img = "/static/img/fdr_severe_new.png";
                var img_alt = "Severe fire danger rating";
            }
            if(fdr['fdr'][h].status == "EXTREME"){
                var img = "/static/img/fdr_extreme_new.png";
                var img_alt = "Extreme fire danger rating";
            }
            if(fdr['fdr'][h].status == "CODE RED"){
                var img = "/static/img/fdr_codered_new.png";
                var img_alt = "Code Red fire danger rating";
            }

            //console.log(data[h]['summary']);
            final_date = tfb['tfb'][h].dateLong
            
            //console.log(date_text);

            // prepare and append the output text
            var rating =  "<div class='panel panel-default'><div class='panel-heading'><b>"+final_date+"</b></div>" +
                        "<div class='panel-body'><img src='"+img+"' alt='"+img_alt+"' title='"+img_alt+"' width='97%'><br>"+
                        tfb_decl_str+"</div></div>";
            $("#display_forecast_fdi_official").append(rating);
        }
        $("#display_forecast_fdi_official").append("<p class='text-center'>For more information please visit the <br><a href='http://www.cfa.vic.gov.au/warnings-restrictions/total-fire-bans-and-ratings/'>CFA website</a></p>");
    });
}

function update_weather_attribution(){
    var weather_source = $('#weather_server option:selected').val();

    if (weather_source == 'aeris') {
        // console.log('aeris');
        $('#forecast-provider').html("AerisWeather");
        $('#forecast-provider-logos').html("<a href='https://www.aerisweather.com/'><img src='static/img/AerisWeather-logo-dark.png' width='100%'></a>");
    } else if (weather_source == 'darksky') {
        // console.log('darksky');
        $('#forecast-provider').html("<a href='https://darksky.net/poweredby/'>Dark Sky</a>");
        $('#forecast-provider-logos').html("");
    } else {
        console.log('NoneType Selected');
    }

}

function generate_error(error){
    $('#flash').html("<div class='alert alert-danger alert-dismissible' role='alert' id='alert_error'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>An Error Occured!</strong>" + error + "</div>");
}