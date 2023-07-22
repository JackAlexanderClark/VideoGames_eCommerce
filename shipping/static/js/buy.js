$(document).ready(function() {

  var inputs = $('input, select');
  // target the next button
  $('.next').prop('disabled', true);

  inputs.on('input', function() {
    var allFilled = true;

    // Check each field to see if it's filled
    inputs.each(function() {
      if ($(this).val() === '') {
        allFilled = false;
      }
    });

    // If all fields are filled, enable the next button and change its color
    if (allFilled) {
      $(this).closest('fieldset').find('.next').prop('disabled', false).css('background', 'green');
    } else {
      $(this).closest('fieldset').find('.next').prop('disabled', true).css('background', '#27AE60');
    }
  });
});
/*
Remember to replace #27AE60 with the original color of your "Next" button if it's different.

This script first gets all the input fields in the form and disables all the "Next" buttons. It then listens for any input events. Whenever the user inputs something, it checks all the input fields to see if they are all filled. If they are, it enables the "Next" button in the current fieldset and changes its color to green. If not, it disables the "Next" button.

Note: This script assumes that the "Next" button should only be enabled when all fields in the entire form are filled. If you want to enable the "Next" button when all fields in the current fieldset are filled, you'll need to adjust the script accordingly.

Please let me know if this helps or if you need further assistance.
*/







