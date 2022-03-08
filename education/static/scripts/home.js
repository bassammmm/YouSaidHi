$(document).ready(function(){

    // $('.homepage-slider').slick({
    //     dots: true,
    //     autoplay: true,
    //     infinite: true,
    //     speed: 700,
    //     fade: true,
    //     cssEase: 'linear'
    // });




});

// document.getElementById('aim-image-1').addEventListener(scroll, function () {
//     TweenMax.to('.aim-image-1', 1, {scaleX: 1, width: '450px'})
// });



// var $window = $(window);
// var $imgOne = $('.aim-image-1');
//
// $window.on('scroll', function () {
//     // console.log("scrolling");
//    var top= $window.scrollTop();
//
//    if($(this).scrollTop()>=120) {
//        $('.aim-image-1').addClass('.animate-aim-image-1');
//        $('.aim-image-2').addClass('.animate-aim-image-2');
//        $('.aim-image-3').addClass('.animate-aim-image-3');
//        $('.aim-image-4').addClass('.animate-aim-image-4');
//    }
//
// });
var $window = $(window);
let $elem = $(".aim-image-1");
let $elem2 = $(".aim-image-2");
let $elem3 = $(".aim-image-3");
let $elem4 = $(".aim-image-4");
let $teacher1 = $('.teacher-div-1');
let $teacher2 = $(".teacher-div-2");
let $teacher3 = $(".teacher-div-3");
let $teacher4 = $(".teacher-div-4");


function isScrolledIntoView(a, $window) {
    let docViewTop = $window.scrollTop();
    let docViewBottom = docViewTop + $window.height();

    let elemTop = a.offset().top;
    let elemBottom = elemTop + a.height();

    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}

function isScrolledOutOfView(a, $window) {
    let docViewTop = $window.scrollTop();
    let docViewBottom = docViewTop + $window.height();

    let elemTop = a.offset().top;
    let elemBottom = elemTop + a.height();

    return !((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}
$(document).on("scroll", function () {
     if (isScrolledIntoView($elem, $window)) {
         $elem.removeClass("animate2-aim-image-1")
         $elem.addClass("animate-aim-image-1")
     }
     if (isScrolledOutOfView($elem,$window)) {
         $elem.removeClass("animate-aim-image-1")
         $elem.addClass("animate2-aim-image-1")
     }
     if (isScrolledIntoView($elem2, $window)) {
         $elem2.removeClass("animate2-aim-image-2")
         $elem2.addClass("animate-aim-image-2")
     }
    if (isScrolledOutOfView($elem2,$window)) {
        $elem2.removeClass("animate-aim-image-2")
        $elem2.addClass("animate2-aim-image-2")
    }

     if (isScrolledIntoView($elem3, $window)) {
         $elem3.removeClass("animate2-aim-image-3")
         $elem3.addClass("animate-aim-image-3")
     }
    if (isScrolledOutOfView($elem3,$window)) {
        $elem3.removeClass("animate-aim-image-3")
        $elem3.addClass("animate2-aim-image-3")
    }


     if (isScrolledIntoView($elem4, $window)) {
         $elem4.removeClass("animate2-aim-image-4")
         $elem4.addClass("animate-aim-image-4")
     }
    if (isScrolledOutOfView($elem4,$window)) {
        $elem4.removeClass("animate-aim-image-4")
        $elem4.addClass("animate2-aim-image-4")
    }


});






//
// if (isScrolledIntoView($teacher1, $window)) {
//
//     $teacher1.addClass("animate-teachers")
// }
//
// if (isScrolledIntoView($teacher2, $window)) {
//     $teacher2.removeClass("unanimate-teachers")
//     $teacher2.addClass("animate-teachers")
// }
// if (isScrolledOutOfView($teacher2,$window)) {
//     $teacher2.removeClass("animate-teachers")
//     $teacher2.addClass("unanimate-teachers")
// }
//
// if (isScrolledIntoView($teacher3, $window)) {
//     $teacher3.removeClass("unanimate-teachers")
//     $teacher3.addClass("animate-teachers")
// }
// if (isScrolledOutOfView($teacher3,$window)) {
//     $teacher3.removeClass("animate-teachers")
//     $teacher3.addClass("unanimate-teachers")
// }
//
//
// if (isScrolledIntoView($teacher4, $window)) {
//     $teacher4.removeClass("unanimate-teachers")
//     $teacher4.addClass("animate-teachers")
// }
// if (isScrolledOutOfView($teacher4,$window)) {
//     $teacher4.removeClass("animate-teachers")
//     $teacher4.addClass("unanimate-teachers")
// }



