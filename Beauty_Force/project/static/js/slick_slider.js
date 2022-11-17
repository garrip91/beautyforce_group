$(document).ready(function(){
    $('.slick-carousel').slick({
        infinite: true,
        variableWidth: true,
        slidesToShow: 3,
        autoplay: true,
        slidesToScroll: 1,
        arrows: true,
        dots: true,
        autoplaySpeed: 3000,
        infinite: true,
        speed: 3000,
    });
    $('.slide-prev').click(function(e){
        $('.slick-carousel').slick('slickPrev');
    } );
    $('.slide-next').click(function(e){
        $('.slick-carousel').slick('slickNext');
    });
});