// Automatically shows on init if cookie isnt set

$('.message .close').on('click', function() {
    $(this).closest('.message').transition('fade');
});

$('.ui.checkbox').checkbox();
