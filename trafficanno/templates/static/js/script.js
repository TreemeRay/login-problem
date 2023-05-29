function ChangePassword() {
    const formID = 'form.pass_change_form';

    $(formID).on('submit', (e) => {
        e.preventDefault();
        var form = $(formID);
        var url = form.attr('action');
        var method = form.attr('method');
        var data = form.serialize();

        $.ajax({
            url: url,
            method: method,
            dataType: 'json',
            data: data,
            success: function (response) {
                var success_message = response.message;
                $('.success-message').text(success_message);
                $(formID + ' input').each((index, el) => {
                    $(el).css('border', '1px solid #ced4da');
                });
                $(formID + ' .invalid-feedback').each((index, el) => {
                    $(el).text('');
                });

                // Clear success message after a 3-second delay
                setTimeout(function() {
                    $('.success-message').text('');
                }, 3000);
            },
            error: function (response) {
                var errors = $.parseJSON(response.responseText);
                var keys = Object.keys(errors.errors);
                var values = Object.values(errors.errors);
                $(formID + ' .success-message').each((index, el) => {
                    $(el).text('');
                });
                $.each(errors.errors, function (key, value) {
                    var field = document.getElementById('id_' + key);
                    var error_value = value[0];
                    field.style.border = "1px solid red";
                    $(field).siblings('.invalid-feedback').text(error_value);
                });
            }
        });
    });

    $(formID + ' input').focus(function () {
        $(formID).removeClass('is-invalid');
        $(formID).siblings('.invalid-feedback').text('');
        $('.success-message').text('');
        $(formID + ' input').each((index, el) => {
            $(el).css('border', '1px solid #ced4da');
        });
    });
}

$(document).ready(() => {
    ChangePassword();
});
