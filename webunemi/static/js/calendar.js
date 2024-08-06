document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: '/events.json',  // Esta es la nueva URL que apunta a tu vista
        eventClick: function (info) {
            document.getElementById('modalTitle').textContent = info.event.title;
            document.getElementById('modalDescription').textContent = info.event.extendedProps.description;
            document.getElementById('modalLocation').textContent = info.event.extendedProps.location;
            document.getElementById('modalDate').textContent = `${info.event.start.toLocaleDateString()} - ${info.event.end.toLocaleDateString()}`;

            var myModal = new bootstrap.Modal(document.getElementById('eventModal'));
            myModal.show();
        }
    });
    calendar.render();
});