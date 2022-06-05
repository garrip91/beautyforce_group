var slideIndex_1 = 1;
showSlides_1(slideIndex_1);

/* Функция увеличивает индекс на 1, показывает следующй слайд*/
function plusCommentSlide() {
    showSlides_1(slideIndex_1 += 1);
}

/* Функция уменьшяет индекс на 1, показывает предыдущий слайд*/
function minusCommentSlide() {
    showSlides_1(slideIndex_1 -= 1);
}

/* Устанавливает текущий слайд */
function currentCommentSlide(n) {
    showSlides_1(slideIndex_1 = n);
}

/* Основная функция слайдера */
function showSlides_1(n) {
    var i;
    var slides = document.getElementsByClassName("item-comment");
    if (n > slides.length) {
      slideIndex_1 = 1
    }
    if (n < 1) {
        slideIndex_1 = slides.length
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex_1 - 1].style.display = "block";
}