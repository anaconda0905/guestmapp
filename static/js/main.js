(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(100).fadeOut("slow");
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Canvas Menu
    $(".canvas__open").on('click', function () {
        $(".offcanvas__menu__wrapper").addClass("show__offcanvas__menu");
        $(".offcanvas__menu__overlay").addClass("active");
    });

    $(".canvas__close, .offcanvas__menu__overlay").on('click', function () {
        $(".offcanvas__menu__wrapper").removeClass("show__offcanvas__menu");
        $(".offcanvas__menu__overlay").removeClass("active");
    });

    /*------------------
        Accordin Active
    --------------------*/
    $('.collapse').on('shown.bs.collapse', function () {
        $(this).prev().addClass('active');
    });

    $('.collapse').on('hidden.bs.collapse', function () {
        $(this).prev().removeClass('active');
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*------------------
        Testimonial Slider
    --------------------*/
    $(".testimonial__slider").owlCarousel({
        loop:true,
        margin:0,
        autoplay:true,
        navText:["<img class='nav-btn' src='/static/img/arrow-left.png'/>","<img class='nav-btn' src='/static/img/arrow-right.png'/>"],
        nav:true,
        dots:true,
        autoplayHoverPause: true,
        autoplaySpeed: 800,
        responsive:{
            0:{
                items:1,
                dots:true,
                nav:false,
            },
            767:{
                items:1,
                dots:true,
                nav:false,
            },
            992:{
                items:3,
                dots:true,
                nav:true,
            },
            1200:{
                items:3,
                dots:true,
                nav:true,
            },
            1500:{
                items:3,
                dots:true,
                nav:true,
            }
        }
    });

    $(".progressguestmapp__slider").owlCarousel({
        loop:true,
        margin:0,
        // autoplay:true,
        navText:["<img class='nav-btn' src='/static/img/arrow-left.png'/>","<img class='nav-btn' src='/static/img/arrow-right.png'/>"],
        nav:true,
        dots:true,
        // autoplayHoverPause: true,
        // autoplaySpeed: 800,
        responsive:{
            0:{
                items:1,
                dots:true,
                nav:false,
            },
            767:{
                items:1,
                dots:true,
                nav:false,
            },
            992:{
                items:3,
                dots:true,
                nav:true,
            },
            1200:{
                items:3,
                dots:true,
                nav:true,
            },
            1500:{
                items:3,
                dots:true,
                nav:true,
            }
        }
    });

    $(".completedguestmapp__slider").owlCarousel({
        loop:true,
        margin:0,
        // autoplay:true,
        navText:["<img class='nav-btn' src='/static/img/arrow-left.png'/>","<img class='nav-btn' src='/static/img/arrow-right.png'/>"],
        nav:true,
        dots:true,
        // autoplayHoverPause: true,
        // autoplaySpeed: 800,
        responsive:{
            0:{
                items:1,
                dots:true,
                nav:false,
            },
            767:{
                items:1,
                dots:true,
                nav:false,
            },
            992:{
                items:3,
                dots:true,
                nav:true,
            },
            1200:{
                items:3,
                dots:true,
                nav:true,
            },
            1500:{
                items:3,
                dots:true,
                nav:true,
            }
        }
    });

    $('#contact_support_btn').on('click', function(event){
        event.preventDefault();
        $('#modal_form_contact').modal('show');
    });

    $('a[href*="#"]').on('click', function (e) {
        e.preventDefault()
      
        $('html, body').animate(
          {
            scrollTop: $($(this).attr('href')).offset().top,
          },
          500,
          'linear'
        )
    });

    $('.dropdown-toggle').dropdown();
})(jQuery);

function doLogin()
{
    $('#modal_form_signup').modal('hide');
    $('#modal_form').modal('show'); // show bootstrap modal
}

function showLogin()
{
    $('#modal_form').modal('show');
}

function goLogin()
{
    $('#modal_form_resetpassword').modal('hide');
    $('#modal_form').modal('show'); // show bootstrap modal
}

function doSignup()
{
    $('#modal_form').modal('hide'); // show bootstrap modal
    $('#modal_form_signup').modal('show'); // show bootstrap modal
}

function doOrderStep1()
{
    // $('#modal_form_order_complete').modal('show');   
    $('#modal_form_order_step1').modal('show');   
}

function backOrderStep1()
{
    $('#modal_form_order_step2').modal('hide');   
    $('#modal_form_order_step1').modal('show');   
}

function doOrderStep2()
{
    $('#modal_form_order_step1').modal('show');   
    $('#modal_form_order_step2').modal('show');   
}

function showOrderStep2()
{
    $('#modal_form_order_step2').modal('show');   
}

function showOrderStep2()
{
    $('#modal_form_order_step2').modal('show');   
}

function doPay(){
    $('#modal_form_order_step2').modal('hide');   
    // $('#modal_form_order_complete').modal('show');   
}

function resetPassword()
{
    $('#modal_form').modal('hide');
    $('#modal_form_resetpassword').modal('show');   
}

function gotoBenefitsSection()
{
    var posY = $(".advantage-section").position();
    $(".advantage-section").scrollTop(posY);
}

function gotoEasystepSection()
{
    var posY = $(".easy-step-section").position();
    $(".easy-step-section").scrollTop(posY);   
}

function gotoFeaturedlistSection()
{
    var posY = $(".recent-guestmapp-section").position();
    $(".recent-guestmapp-section").scrollTop(posY);   
}

function gotoPricingSection()
{
    var posY = $(".pricing-section").position();
    $(".pricing-section").scrollTop(posY);      
}


