$(function() {

    $('#login-form-link').click(function(e) {
		$("#login-form").delay(100).fadeIn(100);
 		$("#user_form").fadeOut(100);
		$('#user-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	$('#user-form-link').click(function(e) {
		$("#user_form").delay(100).fadeIn(100);
 		$("#login-form").fadeOut(100);
		$('#login-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});

});