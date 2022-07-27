$(document).ready(function(){
  $("#close").click(function(){
    $(this).data('clicked', true);
  });
});

$(document).ready(function(e){
  $('.flipped-card').on('click', function(e) {
    e.preventDefault();
    if ($(this).find('.front').is(':visible')){
      $(this).find('.front').hide();
      $(this).find('.back').fadeIn(1000);
    } else if ( $(this).find('#close').data('clicked')){
      $(this).find('.back').hide();
      $(this).find('.front').fadeIn(1000);
      $(this).find('#close').data('clicked', false);
    }
    else {
      return false;
      }
  });
});
