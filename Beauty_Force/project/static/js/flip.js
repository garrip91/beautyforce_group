$(document).ready(function(){
  $("#add_cart").click(            
    function() {
      $(".back").fadeIn(1000)
      $(".front").hide();
    }
  );
});

$(document).ready(function(){
  $("#close").click(            
    function() {
      $(".back").hide();
      $(".front").fadeIn(1000)
    }
  );
});
