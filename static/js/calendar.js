document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        dateClick: function(info) {
            const selectedDate = info.dateStr;
            document.getElementById('entryDate').value = selectedDate;

            $('#entryModal').modal('show');

            $('#view-log-btn').off('click').on('click', function() {
                $('#entryModal').modal('hide');
                fetch(`/food-log/view-entries/?date=${selectedDate}`)
                    .then(response => response.json())
                    .then(data => {
                        $('#existingEntries').html(data.entriesHtml);
                        $('#existingEntries').show();
                        $('#newEntryForm').hide();
                    });
            });

            $('#new-entry-btn').off('click').on('click', function() {
                $('#entryModal').modal('hide');
                $('#newEntryModal').modal('show');
                $('#existingEntries').hide();
                $('#newEntryForm').show();
            });
        }
    });

    calendar.render();
});
