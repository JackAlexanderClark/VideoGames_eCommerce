$(document).ready(function() {
    $(".password-toggle").on('click', function() {

        $(this).toggleClass("fa fa-eye password-toggle");
        var input = $($(this).attr("toggle"));

        if (input.attr("type") == "password") {
            input.attr("type", "text");
        } else {
            input.attr("type", "password");
        }
    });
});