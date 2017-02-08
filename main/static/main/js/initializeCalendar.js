$(document).ready(function() {

    $('#calendar').fullCalendar({
        hiddenDays: [1, 2, 3, 4, 5],
        header: false,
        footer: false,
        firstDay: 1,
        defaultView: 'agendaWeek',
        columnFormat: 'dddd',
        defaultDate: '2000-01-01',
        dayNames: ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
        editable: false,
        handleWindowResize: true,
        displayEventTime: true,
        timeFormat: 'HH:mm',
        contentHeight: "auto",
        views: {
            agenda: {
                allDaySlot: false,

                slotDuration: '01:00:00',
                minTime: '09:00:00',
                maxTime: '17:00:00',
                slotLabelFormat: 'HH:mm',
                slotEventOverlap: false,

            }
        },
    });

    addEvent(-1, 'Monitoria e Palestras', '12:00', '02:00', 1);
    addEvent(-2, 'Monitoria e Palestras', '12:00', '02:00', 2);

    $("input:checkbox").each(function () {
        changeHandler($(this));
    });
});
