$(function() {
    var emailField = $('#email');
    emailField.focus();

    var form = $('#betaRequest');
    form.submit(function(event) {
        var email = emailField.val();
        if (email.indexOf('@') == -1 || email.length == 0 || email.length > 255) {
            $('#emailWrapper').addClass('error');
        } else {
            $.post('/', {email: email}, function() {
                form.replaceWith('' +
                    '<div class="alert alert-success text-center">' +
                    '<strong>Thank you!</strong><br/>Will notify you when we\'ll release it.' +
                    '</div>');
            });
        }
        event.preventDefault();
    });
});