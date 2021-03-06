$(document).ready(function () {
    $(".module-container").on('click', function (e) {
        let target = $(e.target);
        if (target.is(".module")) {
            if (target.attr("data-id")) {
                location.href = `/module/${target.attr("data-id")}`;
            }
        } else if (target.is(".unit") || target.is(".area")) {
            location.href = `/modules?${target.attr('class').split(/\s+/)[0]}=${target.text()}`;
        } else if (target.is(".keyword")) {
            location.href = `/modules?${target.attr('class').split(/\s+/)[0]}=${target.children(".keyword-name").text()}`;
        }
    });
});