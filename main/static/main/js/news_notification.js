// Automatically shows on init if cookie isnt set

function get_nag_message() {
    $.ajax(
    {
        url: get_nag_message_url,
        type: 'get',
        success: function(data) {
            $("#mod_edit_nag_message").val(data['message']);
            $("#mod_edit_nag_enable").checkbox('uncheck');
            $("#cookie_nag_text").html(data['message']);
            if (data['enable'] == true) {
                $("#mod_edit_nag_enable").checkbox('check');
                $('#cookie_nag').nag({
                    key      : data['id'],
                    value    : true
                });
            }
        }
    })
}

function update_nag_message() {
    $("#nag_form").removeClass('success');
    $("#nag_form").removeClass('error');
    $("#nag_form").addClass('loading');
    message = $("#mod_edit_nag_message").val();
    enable = false;
    if ($("#mod_edit_nag_enable").checkbox('is checked'))
        enable = true;
    $.ajax(
    {
        url: update_nag_message_url,
        type: 'post',
        data: {
            csrfmiddlewaretoken: csrf,
            message: message,
            enable: enable
        },
        success: function(data) {
            get_nag_message();
            $("#nag_form").removeClass('loading');
            $("#nag_form").addClass('success');
        },
        error: function(data) {
            get_nag_message();
            $("#nag_form").removeClass('loading');
            $("#nag_form").addClass('error');
        }
    })
}

get_nag_message();
