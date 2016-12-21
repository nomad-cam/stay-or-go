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

    if (district_check == 0){
        generate_error("<li>No Fire District has been selected</li>");
        return;
    }

    var district = $('#fire_district option:selected').text();
    //console.log(district);

    //var FEED_URL = "http://www.cfa.vic.gov.au/restrictions/tfbfdrforecast_rss.xml";
    var FEED_URL = "/api/fx/forecast/fdr";
    $.get(FEED_URL, function(data){
        //console.log(data);
        $("#display_forecast_fdi_official").html("<p class='text-center'><small>Issued: " + data[data.length-1]['updated-local'] + "</small><br><h3 class='text-center'>"+district+" Forecast District</h3></p>");
        for(var h = 0; h < data.length - 1; h++){
            var tfb_index1 = data[h]['summary'].indexOf(">"+district);
            var tfb_index2 = data[h]['summary'].indexOf("<",tfb_index1);
            //console.log(tfb_index1,tfb_index2);

            var fdi_index1 = data[h]['summary'].indexOf(">"+district,tfb_index2);
            var fdi_index2 = data[h]['summary'].indexOf("<",fdi_index1);
            //console.log(fdi_index1,fdi_index2);

            var tfb_text = data[h]['summary'].substr(tfb_index1,(tfb_index2-tfb_index1));
            var fdi_text = data[h]['summary'].substr(fdi_index1,(fdi_index2-fdi_index1));
            //console.log(tfb_text);
            //console.log(fdi_text);
            var tfb_decl = tfb_text.split(":");
            var fdi_decl = fdi_text.split(": ");
            //console.log(tfb_decl[1]);
            //console.log(fdi_decl[1]);

            //Check for a declared TFB otherwise default to No TFB
            var tfb_decl_str = "<p class='text-center'>No TFB Declared<br>(Restrictions may still apply)</p>";
            //console.log(tfb_decl[1].indexOf("Yes"));
            if (tfb_decl[1].indexOf("Yes") >= 0){
                tfb_decl_str = "<p class='text-center'><img src='/static/img/tfb_icon.gif'> TFB DECLARED</p>";
            }

            //console.log(fdi_decl[1]);
            // determine which image to display
            var img = "/static/img/fdr_null_new.png";
            var img_alt = "no fire danger rating";

            if(fdi_decl[1] == "LOW-MODERATE"){
                var img = "/static/img/fdr_low_new.png";
                var img_alt = "Low moderate fire danger rating";
            }
            if(fdi_decl[1] == "HIGH"){
                var img = "/static/img/fdr_high_new.png";
                var img_alt = "High fire danger rating";
            }
            if(fdi_decl[1] == "VERY HIGH"){
                var img = "/static/img/fdr_veryhigh_new.png";
                var img_alt = "Very High fire danger rating";
            }
            if(fdi_decl[1] == "SEVERE"){
                var img = "/static/img/fdr_severe_new.png";
                var img_alt = "Severe fire danger rating";
            }
            if(fdi_decl[1] == "EXTREME"){
                var img = "/static/img/fdr_extreme_new.png";
                var img_alt = "Extreme fire danger rating";
            }
            if(fdi_decl[1] == "CODE RED"){
                var img = "/static/img/fdr_codered_new.png";
                var img_alt = "Code Red fire danger rating";
            }

            //console.log(data[h]['summary']);
            var date_index1 = data[h]['summary'].indexOf("<br />");
            var date_index2 = data[h]['summary'].indexOf("</p>",date_index1);
            var date_text = data[h]['summary'].substr(date_index1+6,(date_index2-date_index1));
            var d = date_text.split(" ");
            final_date = d[0]+" "+d[1]+" "+d[2]+" "+d[3]+" "+d[4];
            if (d[4] == "is"){
                final_date = d[0]+" "+d[1]+" "+d[2]+" "+d[3];
            }

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

function generate_error(error){
    $('#flash').html("<div class='alert alert-danger alert-dismissible' role='alert' id='alert_error'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>An Error Occured!</strong>" + error + "</div>");
}