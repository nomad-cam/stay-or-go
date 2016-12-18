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

//$(document).ready();
$(load_station_list());
//