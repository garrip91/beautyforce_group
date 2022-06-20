$(document).ready(function() {
	$('#add_to_cart').ajaxForm({
		dataType:  'json',
		success:   processJson
	});
});
function processJson(data, statusText, xhr, $form) {
	if (data['result'] == 'success') {
		 $('#add_to_cart')[0].reset();
		 $('#add_to_cart_modal').modal('show');
	}
	else if (data['result'] == 'error') {
		$('#add_to_cart')[0].reset();
		$("#error_span").text(data['response']);
		$('#add_to_cart_modal_error').modal('show');
	}
}