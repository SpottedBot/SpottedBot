function addEvent(id, name, start, duration, day) {
    var newEvent = new Object();
    newEvent.title = name;
    newEvent.start = moment('2000-01-' + day + ' ' + start.toString(), "YYYY-MM-DD HH:mm");
    newEvent.end = moment('2000-01-' + day + ' ' + start.toString(), "YYYY-MM-DD HH:mm").add(duration.match(/[0-9]+/g)[0], 'hours');
    newEvent.allDay = false;
    newEvent.id = id;

    var colors = ["#F44336", "#E91E63", "#9C27B0", "#3F51B5", "#2196F3", "#03A9F4", "#00BCD4", "#009688", "#4CAF50", "#8BC34A", "#CDDC39", "#FFEB3B", "#FF9800", "#FF5722", "#795548", "#9E9E9E", "#607D8B"];
    newEvent.color = colors[Math.floor(Math.random()*colors.length)];

    $('#calendar').fullCalendar('renderEvent', newEvent);
};

function removeEvent(id) {
    $('#calendar').fullCalendar('removeEvents', id);
};

function changeHandler(t) {
    var id = Number(t.attr('value'));

    if (t.is(':checked')) {

        addEvent(id, options[id].name, options[id].start, options[id].duration, options[id].day)
    } else {
      removeEvent(id)
    }
}
