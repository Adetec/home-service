$(document).ready(function(){
    $('.carousel').carousel()

    $('#action-requests').click(() => {
        $('#requests').toggleClass('hide');
    });
    $('#action-services').click(() => {
        $('#services').toggleClass('hide');
    });
    $('#action-edit-profile').click(() => {
        $('#edit-profile').toggleClass('hide');
    });
});

