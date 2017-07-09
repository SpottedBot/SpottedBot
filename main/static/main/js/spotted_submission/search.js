$('#target_name .typeahead').typeahead(null, {
    // Initialize typeahead
    name: 'targets',
    limit: 10,
    displayKey: 'name',
    source: targets.ttAdapter(),
    templates: {
        suggestion: function (data) {
            return '<div><img style="vertical-align:middle" src="' + data.picture + '"/>  <span><b>' + data.name + '</b></span></div>';
        },
        empty: [
        '<div style="color: black; text-align: center; margin: 20px;" class="empty-message">',
        'Nenhum crush com esse nome cadastrado :(',
        '</div>'
        ].join('\n'),
    }
});

// Set selected user to hidden input
$('#target_name .typeahead').on('typeahead:selected', function (e, datum) {
    $(".tt-menu").removeClass("tt-menu-keep-open");
    $("#id_target_id").val(datum['id']);
    if (user_is_authenticated) {
        $("#target_found_checkbox_div").show();
        $("#target_found_tip").text("Crush selecionado!");
    }
});

// Manually trigger typeahead
function manual_trigger(text) {
    $('.typeahead').typeahead('open');
    $('.typeahead').typeahead('val', text);
return 0;
};

// Perform manual search using bloodhoud
function manual_search(text) {
    var manual_search_results;
    function sync(datums) {
        manual_search_results = datums;
    }
    targets.search(text, sync);
    return manual_search_results;
};
