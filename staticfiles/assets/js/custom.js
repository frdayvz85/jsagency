(function ($) {
  "use strict";

  // PRE LOADER
  $(window).load(function () {
    $(".preloader").fadeOut(1000); // set duration in brackets
  });

  // PRE LOADER 2
  $(window).load(function () {
    $(".tela").fadeOut(1000); // set duration in brackets
  });

  // MENU
  $(".navbar-collapse a").on("click", function () {
    $(".navbar-collapse").collapse("hide");
  });

  $(window).scroll(function () {
    if ($(".navbar").offset().top > 50) {
      $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
      $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
  });

  // HOME SLIDER & COURSES & CLIENTS
  $(".home-slider").owlCarousel({
    animateOut: "fadeOut",
    items: 1,
    loop: true,
    dots: false,
    autoplayHoverPause: false,
    autoplay: true,
    smartSpeed: 1000,
  });

  $(".owl-courses").owlCarousel({
    animateOut: "fadeOut",
    loop: true,
    autoplayHoverPause: false,
    autoplay: false,
    dots: false,
    nav: true,
    navText: [
      '<i class="fa fa-angle-left"></i>',
      '<i class="fa fa-angle-right"></i>',
    ],
    responsiveClass: true,
    responsive: {
      0: {
        items: 1,
      },
      1000: {
        items: 3,
      },
    },
  });

  $(".owl-client").owlCarousel({
    animateOut: "fadeOut",
    loop: true,
    autoplayHoverPause: false,
    autoplay: true,
    smartSpeed: 1000,
    responsiveClass: true,
    responsive: {
      0: {
        items: 1,
      },
      1000: {
        items: 3,
      },
    },
  });

  // SMOOTHSCROLL
  $(function () {
    $(".custom-navbar a, #home a").on("click", function (event) {
      var $anchor = $(this);
      $("html, body")
        .stop()
        .animate(
          {
            scrollTop: $($anchor.attr("href")).offset().top - 49,
          },
          1000
        );
      event.preventDefault();
    });
  });

  // UPLOAD IMG
  $("#file1").on("change", function () {
    var files = !!this.files ? this.files : [];
    if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support

    if (/^image/.test(files[0].type)) {
      // only image file
      var reader = new FileReader(); // instance of the FileReader
      reader.readAsDataURL(files[0]); // read the local file

      reader.onloadend = function () {
        // set image data as background of div
        $("img.upload-img").attr("src", reader.result).removeClass("default");
      };
    }
  });

  $("#file2").on("change", function () {
    var files = !!this.files ? this.files : [];
    if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support

    if (/^image/.test(files[0].type)) {
      // only image file
      var reader = new FileReader(); // instance of the FileReader
      reader.readAsDataURL(files[0]); // read the local file

      reader.onloadend = function () {
        // set image data as background of div
        $("img.upload-img1").attr("src", reader.result).removeClass("default");
      };
    }
  });
  
  $(function () {
    $("div.comment-load").slice(0, 4).show();
    $("#loadMore").on("click", function (e) {
      e.preventDefault();
      $("div.comment-load:hidden").slice(0, 4).slideDown();
      if ($("div.comment-load:hidden").length == 0) {
        $("#loadMore").addClass("none");
        $("#load").fadeOut("slow");
      }
    });
  });
})(jQuery);

