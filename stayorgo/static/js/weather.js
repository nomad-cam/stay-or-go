//$(document).ready();
$(load_station_list());
//

$('#forecast_fdi').click(function () {
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
            var option = "";
            for (var j = 0; j < data.length; j++){
                option += "<option value='" + data[j]["bom-id"] + "'>" + data[j]["name"] + "</option>";
            }
            $('#weather_station').append(option);
        }
    });
}


function fetch_fdi_forecast(){
    //
    //var FEED_URL = "http://www.cfa.vic.gov.au/restrictions/tfbfdrforecast_rss.xml";
    var FEED_URL = "/api/fx/forecast/fdr";
    $.get(FEED_URL, function(data){
        console.log(data);
    });
}