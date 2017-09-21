// Main JS function to change the content of second list box "DestDir" based on a change on the first list box "EnvName"...
$(document).ready(function() {
    $(".EnvName").change(function() { 
        // grab value
        var envName = $(".EnvName").val();        

        // send value via GET to URL /<dirlist>
        var get_request = $.ajax({
            type: 'POST',
            //data: 'JSON.stringify([envName])',
            url: '/dirlist/' + envName + '/',
        });

        // handle response
        get_request.done(function(data){
            // data
            console.log(data);
            // add values to list 
            //var option_list = [["", "Select another directory"]].concat(data);
            var option_list = data;
            $(".DestDir").empty();
                for (var i = 0; i < option_list.length; i++) {
                    $(".DestDir").append(
                    $("<option></option>").attr("value", option_list[i]).text(option_list[i]));
                }
                // show model list
                $("#DestDir").show();
        });
    });
});