$(document).ready(function () {
    const token = $("input[name=csrfmiddlewaretoken]").val();

    $('.btn-delete').click(function () {
        const eventId = $(this).attr('event-id');
        const confirmDelete = confirm('Bạn có xóa không');

        if (confirmDelete) {
            $.ajax({
                method: "POST",
                url: `/api/v1/event/${eventId}`,
                headers: {
                    'X-CSRFToken': `${token}`
                }
            }).done(function (msg) {
                window.location.reload()
            }).fail(function (ms) {
                alert("Lỗi: " + ms);
            });
        }
    })

    $('.btn-update').click(function () {
        const eventId = $(this).attr('event-id');
        const confirmUpdate = confirm('Bạn có xóa không');

        if (confirmUpdate) {
            $.ajax({
                method: "PUT",
                url: `/api/v1/event/${eventId}`,
                headers: {
                    'X-CSRFToken': `${token}`
                }
            }).done(function (msg) {
                window.location.reload()
            }).fail(function (ms) {
                alert("Lỗi: " + ms);
            });
        }
    })
});
