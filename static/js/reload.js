$(document).ready(function()
{
  var append_increment = 0;
    setInterval(function() {
        $.ajax({
            type: "GET",
            url: 'get_more_tables' ,  // URL to your view that serves new info
            data: {'append_increment': append_increment}
        })
        .done(function(response) {
            $("#_appendHere").empty();
            $('#_appendHere').append(response);
            append_increment += 10;
        });
    }, 10000)
});
/*setTimeout(function(){
   window.location.reload(1);
}, 2000);*/
   /* alert("hi");
     var append_increment = 0;
        setInterval(function() {
            $.ajax({
                type: "GET",
                url:  {% url 'get_more_tables' %},
                data: {'append_increment': append_increment}
            })
            .done(function(response) {
                $('#_appendHere').append(response);
                append_increment += 10;
            });
        }, 2000)*/

