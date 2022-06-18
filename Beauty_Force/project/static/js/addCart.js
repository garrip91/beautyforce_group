		$(function() {
			$(".ad_to_cart").submit(function(event) {
				// Stop form from submitting normally
				event.preventDefault();
				var friendForm = $(this);
				// Send the data using post
				var posting = $.post( friendForm.attr('action'), friendForm.serialize() );
				// if success:
				posting.done(function(data) {
					$('#add_to_cart_modal').modal('show')
				});
				// if failure:
				posting.fail(function(data) {
					// 4xx or 5xx response, alert user about failure
				});
			});
		});