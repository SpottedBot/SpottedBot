$('.ui.file.input').find('input:text, .ui.button').on('click', function(e) {
    $(e.target).parent().find('input:file').click();
});

$('input:file', '.ui.file.input').on('change', function(e) {
    var file_field = $("#imgur_file");
    var name = '';

    for (var i=0; i<e.target.files.length; i++) {
        name += e.target.files[i].name + ', ';
    }

    name = name.replace(/,\s*$/, '');

    $('input:text', file_field.parent()).val(name);

    var file = file_field[0].files[0];
    var formData = new FormData();
    formData.set('picture', file); //append file to formData object
    console.log(csrf_token);
    formData.set('csrfmiddlewaretoken', csrf_token);

    // Check if the user selected a file
    if (typeof file == 'undefined')
        return;
    $("#imgur_button").addClass("loading");
    $("#imgur_button").prop('disabled', true);
    $("#message_button").prop('disabled', true);
    $("#imgur_info").text("Fazendo upload...");
    $.ajax({
        url: "/imgur_upload/",
        type: "POST",
        data: formData,
        processData: false, //prevent jQuery from converting your FormData into a string
        contentType: false, //jQuery does not add a Content-Type header for you
        success: function (msg) {
            if (msg['ok']) {
                $("#imgur_button").removeClass("loading");
                $("#message_button").prop('disabled', false);
                $("#imgur_button").prop('disabled', false);
                $("#id_attachment").val(msg['url']);
                $("#imgur_info").text("Sucesso!");
            }
            else {
                $("#imgur_button").removeClass("loading");
                $("#message_button").prop('disabled', false);
                $("#imgur_button").prop('disabled', false);
                $("#imgur_info").text(msg['error']);
                $('input:text', file_field.parent()).val("Oops!");
            }
        }
    });
});
