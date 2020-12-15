$(document).ready(function () {
    $(".like_btn").click(function (event) {
        event.preventDefault()
        var ansid = $(this).attr('id');
        $.ajax({
            url: $(this).data('url'),
            type: 'POST',
            data: {
                'post_id': $('#' + ansid).val(),
                'csrfmiddlewaretoken': $(this).data('csrf'),
                'action': 'post'
            },
            success: function (response) {
                // document.getElementById("like_count").innerHTML = response['result']
                $('#like_count' + ansid).html(response['result']);
                // console.log(response['stated'])
                if (response['flag']){
                    $('#' + ansid).addClass('text-danger animated zoomIn');
                }else{
                    $('#' + ansid).removeClass('text-danger animated zoomIn');
                } 
                console.log($('#like_count' + ansid))
            },
            error: function (rs, e) {
                console.log(rs.response)
            }
        });
    });
});
