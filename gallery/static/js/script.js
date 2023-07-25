$(document).ready(function() {
    if ($('#msform').length) {  // check user has form
        $('.next').attr('disabled', 'disabled');

        setInterval(function() {
            $('fieldset').each(function() {
                var inputs = $(this).find('input, select');
                var empty = inputs.filter(function() {
                    return !this.value;
                });
                if (!empty.length) {
                    $(this).find('.next').removeAttr('disabled');
                } else {
                    $(this).find('.next').attr('disabled', 'disabled');
                }
            });
        }, 1000);
    }
});
