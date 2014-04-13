$(document).ready(function(){

   $('#username_explain').click(function(){
   	$(this).toggleClass('active');
	});

	$('#explain_title').click(function(){
		if ($(this).parent().class == 'active') {
   			$(this).parent().removeClass('active');			
   		}
	});

   $('#signup_modal_on, #cancel_button_chat, #signup_button_chat').click(function(){
      $('#signup_modal').toggleClass('active');
   });

	$(document).click(function(e){
		if (!$(e.target).is('#username_explain') &&
			!$(e.target).is('#explain_title')) {
	   		$('#username_explain').removeClass('active');
		}
	});

	$('button').click(function(e){
		if ($(this).is($('#signup_button'))) {
			$(this).text(function(i, text){
				return text === 'Cancel' ? 'Sign Up' : 'Cancel';
			});
			$('#login_button').text(function(i, text){
				return text === 'Sign Up' ? 'Log In' : 'Sign Up'
			});
			$('#login_small').toggleClass('filling');
			$('#signup_fields').toggleClass('filling');
 	   }
  	});

   $('#send_msg_button').click(function() {
		what_the_user_typed = $('textarea').val();
		$('#chatreceive').append('<div class="clearfix"><div class="message_box">' + what_the_user_typed + '</div></div>');
		$('textarea').val('');
		$("#chatreceive").scrollTop($("#chatreceive")[0].scrollHeight);
	});

	$('textarea').keypress(function(event) {
	   if (event.which == 13) {
	      event.preventDefault();
	      what_the_user_typed = $('textarea').val();
			$('#chatreceive').append('<div class="clearfix"><div class="message_box">' + what_the_user_typed + '</div></div>');
			$('textarea').val('');
			$("#chatreceive").scrollTop($("#chatreceive")[0].scrollHeight);
	   }
	});

});