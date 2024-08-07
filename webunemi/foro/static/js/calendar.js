document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: '/all_events/',
        eventClick: function (info) {
            info.jsEvent.preventDefault();

            document.getElementById('eventTitle').textContent = info.event.title;
            document.getElementById('eventDescription').textContent = info.event.extendedProps.description || 'No hay descripción disponible';
            document.getElementById('eventLocation').textContent = info.event.extendedProps.location || 'No se especificó ubicación';

            var myModal = new bootstrap.Modal(document.getElementById('eventModal'));
            myModal.show();

            // Agregar evento para cerrar el modal
            document.querySelector('#eventModal .btn-close').addEventListener('click', function () {
                myModal.hide();
            });

            document.querySelector('#eventModal .btn-secondary').addEventListener('click', function () {
                myModal.hide();
            });
        }
    });
    calendar.render();
});