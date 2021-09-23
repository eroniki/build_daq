function ajax_call(url, data, type = "GET") {
    $.ajax({
        url: url,
        type: type,
        data: data
    }).fail(function (result) {
        extra = $("<a>", {
            "href": "javascript:window.location.href=window.location.href",
            "text": "Reload the page?"
        });
        toast_alert(result.responseText, Date.now(), false, extra);
    }).done(function (result) {
        if (typeof (result) == "object") {
            result = JSON.stringify(result);
        }
        toast_alert(result, Date.now());
    }).always(function () {
        // add something here
    });
}

function toast_alert(msg, time, autohide = true, extra = undefined) {
    var $toast = $("<div>", {
        "id": time.toString(),
        "class": "toast",
        "data-animation": true,
        "data-autohide": autohide,
        "data-delay": 5000,
        "role": "alert",
        "aria-live": "assertive",
        "aria-atomic": true
    });

    var $toast_header = $("<div>", { "class": "toast-header" })
        .append($("<i>", {
            "class": "bi bi-bell-fill"
        })).append($("<strong>", {
            "class": "mr-auto",
            "text": "System Response ".concat(String.fromCodePoint(parseInt("1F44B", 16)))
        })).append($("<small>", {
            "class": "text-muted",
            "text": time,
        })).append($("<button>", {
            "id": time.toString().concat("close_toast"),
            "class": "ml-2 mb-1 close",
            "type": "button",
            "data-dismiss": "toast",
            "aria-label": "Close",
        }).append($("<span>", {
            "aria-hidden": "true",
            "text": "×"
        })));

    var $toast_body = $("<div>", {
        "class": "toast-body",
        "text": msg
    });

    if (typeof (extra) == "string" || typeof (extra) == "object") {
        $toast_body.append(["<hr>", extra]);
    }

    $toast.prepend($toast_header).append($toast_body);
    $('#toast_container').prepend($toast);
    $('.toast').toast("show");
    $('.toast').on('hidden.bs.toast', function (event) {
        this.remove();
    });
}


// make all tooltips visible
$(document).ready(function () {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
});
// Make Select All checkbox functional in experiments template
$(document).ready(function () {
    $("#select_all_check").click(function () {
        $('input:checkbox').not(this).prop('checked', this.checked);
    });
});

$(document).ready(function () {
    $(document).on("click", ".sys_link", function (event) {
        var id = $(this).attr("id");
        switch (id) {
            case "#status_rooms":
                ajax_call("/status_rooms", null, "GET");
                break;
            case "#reload_settings":
                ajax_call("/reload_settings", null, "GET");
                break;
            default:
            // code block
        }
    });
});

// Stuff needed in the experiments.html
$(document).ready(function () {
    $("a.experiment_action").click(function (event) {
        event.preventDefault();
        var id = $(this).attr('id').split("_")[0];
        var form = $("#" + id.toString() + "_form");
        var data = $(form).serialize();
        var href = $(this).attr('href');
        ajax_call(href, data, "GET");
    });
});
