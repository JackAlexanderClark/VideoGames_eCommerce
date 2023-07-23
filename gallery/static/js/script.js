$(document).ready(function() {
    // disable next button until form has data
    $('.next').attr('disabled', 'disabled');
    $('input, select').on('keyup change', function() {
        var currentFieldset = $(this).parents('fieldset');
        var inputs = currentFieldset.find('input, select');
        var empty = inputs.filter(function() {
            return !this.value;
        });
        if (!empty.length) {
            currentFieldset.find('.next').removeAttr('disabled');
        } else {
            currentFieldset.find('.next').attr('disabled', 'disabled');
        }
    });
});