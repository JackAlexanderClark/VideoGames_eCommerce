$(document).ready(function() {
  $('.password-toggle').click(function() {
    // Get the password field
    var passwordField = $(this).siblings('.password');

    var passwordFieldType = passwordField.attr('type');
    passwordField.attr('type', passwordFieldType === 'password' ? 'text' : 'password');

    $(this).toggleClass('fa-eye fa-eye-slash');
  });
});