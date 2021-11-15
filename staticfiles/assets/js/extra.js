const close = document.querySelector('.myAlert .fas');
const alert = document.querySelector('.myAlert');

close?.addEventListener('click',()=> {
    alert.classList.add('dontShow')
})
setTimeout(() => {
    alert?.classList.add('dontShow')
}, 15000);

let tabContent = document.querySelectorAll(".container__inner");
let tabItem = document.querySelectorAll(".container__item");

// For each element with class 'container__item'
for (let i = 0; i < tabItem.length; i++) {
  // if the element was hovered
  //you can replace mouseover with click
  tabItem[i].addEventListener("click", () => {
    // Add to all containers class 'container__inner_hidden'
    tabContent.forEach((item) => {
      item.classList.add("container__inner_hidden");
    });
    // Clean all links from class 'container__item_active'
    tabItem.forEach((item) => {
      item.classList.remove("container__item_active");
    });
    // Make visible correct tab content and add class to item
    tabContent[i].classList.remove("container__inner_hidden");
    tabItem[i].classList.add("container__item_active");
  });
}



(function() {
    var toggleElement;
  
    toggleElement = function($el, type) {
      if (type != null) {
        if (type === 'open') {
          $el.addClass('panel-element-open');
          $el.siblings('.panel-element').removeClass('panel-element-open');
        } else if (type === 'close') {
          $el.removeClass('panel-element-open');
        }
      } else {
        if ($el.hasClass('panel-element-open')) {
          toggleElement($el, 'close');
        } else {
          toggleElement($el, 'open');
        }
      }
      return null;
    };
  
    $(document).ready(function() {
      var hammertime;
      $('.btn1').click(function() {
        var $parent;
        $parent = $(this).parents('.panel-element');
        if ($(this).hasClass('btn-heart')) {
          if ($parent.hasClass('panel-element-hearted')) {
            return $parent.removeClass('panel-element-hearted');
          } else {
            $parent.addClass('panel-element-hearted');
            return toggleElement($parent, 'close');
          }
        } else if ($(this).hasClass('btn-hide')) {
          toggleElement($parent, 'close');
          return $parent.delay(200).fadeOut(300);
        } else if ($(this).hasClass('btn-more')) {
          if (!hammertime) {
            return toggleElement($parent);
          }
        }
      });
      if ($(window).width() < 800) {
        // Mobile swiping with Hammer.js
        // https://hammerjs.github.io
        hammertime = $('.panel-element .element-content').hammer();
        return hammertime.on('swipeleft swiperight tap', function(e) {
          var $parent;
          $parent = $(e.currentTarget).parent();
          if (e.type === 'tap') {
            return toggleElement($parent);
          } else if (e.type === 'swipeleft') {
            if (!$parent.hasClass('panel-element-open')) {
              return toggleElement($parent, 'open');
            }
          } else {
            if ($parent.hasClass('panel-element-open')) {
              return toggleElement($parent, 'close');
            }
          }
        });
      }
    });
  
  }).call(this);
  
  //# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiPGFub255bW91cz4iXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7QUFBQSxNQUFBOztFQUFBLGFBQUEsR0FBZ0IsUUFBQSxDQUFDLEdBQUQsRUFBTSxJQUFOLENBQUE7SUFFZixJQUFHLFlBQUg7TUFFQyxJQUFHLElBQUEsS0FBUyxNQUFaO1FBQ0MsR0FBRyxDQUFDLFFBQUosQ0FBYSxvQkFBYjtRQUNBLEdBQUcsQ0FBQyxRQUFKLENBQWEsZ0JBQWIsQ0FBOEIsQ0FBQyxXQUEvQixDQUEyQyxvQkFBM0MsRUFGRDtPQUFBLE1BSUssSUFBRyxJQUFBLEtBQVEsT0FBWDtRQUNKLEdBQUcsQ0FBQyxXQUFKLENBQWdCLG9CQUFoQixFQURJO09BTk47S0FBQSxNQUFBO01BV0MsSUFBRyxHQUFHLENBQUMsUUFBSixDQUFhLG9CQUFiLENBQUg7UUFDQyxhQUFBLENBQWMsR0FBZCxFQUFtQixPQUFuQixFQUREO09BQUEsTUFBQTtRQUdDLGFBQUEsQ0FBYyxHQUFkLEVBQW1CLE1BQW5CLEVBSEQ7T0FYRDs7QUFnQkEsV0FBTztFQWxCUTs7RUFvQmhCLENBQUEsQ0FBRSxRQUFGLENBQVcsQ0FBQyxLQUFaLENBQWtCLFFBQUEsQ0FBQSxDQUFBO0FBRWxCLFFBQUE7SUFBQyxDQUFBLENBQUUsTUFBRixDQUFTLENBQUMsS0FBVixDQUFnQixRQUFBLENBQUEsQ0FBQTtBQUVqQixVQUFBO01BQUUsT0FBQSxHQUFVLENBQUEsQ0FBRSxJQUFGLENBQUksQ0FBQyxPQUFMLENBQWEsZ0JBQWI7TUFFVixJQUFHLENBQUEsQ0FBRSxJQUFGLENBQUksQ0FBQyxRQUFMLENBQWMsV0FBZCxDQUFIO1FBRUMsSUFBRyxPQUFPLENBQUMsUUFBUixDQUFpQix1QkFBakIsQ0FBSDtpQkFDRSxPQUFPLENBQUMsV0FBUixDQUFvQix1QkFBcEIsRUFERjtTQUFBLE1BQUE7VUFHRSxPQUFPLENBQUMsUUFBUixDQUFpQix1QkFBakI7aUJBQ0EsYUFBQSxDQUFjLE9BQWQsRUFBdUIsT0FBdkIsRUFKRjtTQUZEO09BQUEsTUFRSyxJQUFHLENBQUEsQ0FBRSxJQUFGLENBQUksQ0FBQyxRQUFMLENBQWMsVUFBZCxDQUFIO1FBQ0osYUFBQSxDQUFjLE9BQWQsRUFBdUIsT0FBdkI7ZUFDQSxPQUFPLENBQUMsS0FBUixDQUFjLEdBQWQsQ0FBa0IsQ0FBQyxPQUFuQixDQUEyQixHQUEzQixFQUZJO09BQUEsTUFJQSxJQUFHLENBQUEsQ0FBRSxJQUFGLENBQUksQ0FBQyxRQUFMLENBQWMsVUFBZCxDQUFIO1FBQ0osSUFBRyxDQUFJLFVBQVA7aUJBQ0MsYUFBQSxDQUFjLE9BQWQsRUFERDtTQURJOztJQWhCVSxDQUFoQjtJQW9CQSxJQUFHLENBQUEsQ0FBRSxNQUFGLENBQVMsQ0FBQyxLQUFWLENBQUEsQ0FBQSxHQUFvQixHQUF2Qjs7O01BSUMsVUFBQSxHQUFhLENBQUEsQ0FBRSxpQ0FBRixDQUFvQyxDQUFDLE1BQXJDLENBQUE7YUFFYixVQUFVLENBQUMsRUFBWCxDQUFjLDBCQUFkLEVBQTBDLFFBQUEsQ0FBQyxDQUFELENBQUE7QUFFNUMsWUFBQTtRQUFHLE9BQUEsR0FBVSxDQUFBLENBQUUsQ0FBQyxDQUFDLGFBQUosQ0FBa0IsQ0FBQyxNQUFuQixDQUFBO1FBRVYsSUFBRyxDQUFDLENBQUMsSUFBRixLQUFVLEtBQWI7aUJBQ0MsYUFBQSxDQUFjLE9BQWQsRUFERDtTQUFBLE1BR0ssSUFBRyxDQUFDLENBQUMsSUFBRixLQUFVLFdBQWI7VUFFSixJQUFHLENBQUksT0FBTyxDQUFDLFFBQVIsQ0FBaUIsb0JBQWpCLENBQVA7bUJBQ0MsYUFBQSxDQUFjLE9BQWQsRUFBdUIsTUFBdkIsRUFERDtXQUZJO1NBQUEsTUFBQTtVQU1KLElBQUcsT0FBTyxDQUFDLFFBQVIsQ0FBaUIsb0JBQWpCLENBQUg7bUJBQ0MsYUFBQSxDQUFjLE9BQWQsRUFBdUIsT0FBdkIsRUFERDtXQU5JOztNQVBvQyxDQUExQyxFQU5EOztFQXRCaUIsQ0FBbEI7QUFwQkEiLCJzb3VyY2VzQ29udGVudCI6WyJ0b2dnbGVFbGVtZW50ID0gKCRlbCwgdHlwZSkgLT5cblxuXHRpZiB0eXBlP1xuXG5cdFx0aWYgdHlwZSBpcyAgJ29wZW4nXG5cdFx0XHQkZWwuYWRkQ2xhc3MgJ3BhbmVsLWVsZW1lbnQtb3Blbidcblx0XHRcdCRlbC5zaWJsaW5ncygnLnBhbmVsLWVsZW1lbnQnKS5yZW1vdmVDbGFzcyAncGFuZWwtZWxlbWVudC1vcGVuJ1xuXG5cdFx0ZWxzZSBpZiB0eXBlIGlzICdjbG9zZSdcblx0XHRcdCRlbC5yZW1vdmVDbGFzcyAncGFuZWwtZWxlbWVudC1vcGVuJ1xuXG5cdGVsc2VcblxuXHRcdGlmICRlbC5oYXNDbGFzcyAncGFuZWwtZWxlbWVudC1vcGVuJ1xuXHRcdFx0dG9nZ2xlRWxlbWVudCAkZWwsICdjbG9zZSdcblx0XHRlbHNlXG5cdFx0XHR0b2dnbGVFbGVtZW50ICRlbCwgJ29wZW4nXG5cblx0cmV0dXJuIG51bGxcblxuJChkb2N1bWVudCkucmVhZHkgLT5cblxuXHQkKCcuYnRuJykuY2xpY2sgLT5cblxuXHRcdCRwYXJlbnQgPSAkKEApLnBhcmVudHMgJy5wYW5lbC1lbGVtZW50J1xuXG5cdFx0aWYgJChAKS5oYXNDbGFzcyAnYnRuLWhlYXJ0J1xuXHRcdFx0XG5cdFx0XHRpZiAkcGFyZW50Lmhhc0NsYXNzICdwYW5lbC1lbGVtZW50LWhlYXJ0ZWQnXG5cdFx0XHRcdFx0JHBhcmVudC5yZW1vdmVDbGFzcyAncGFuZWwtZWxlbWVudC1oZWFydGVkJ1xuXHRcdFx0XHRlbHNlXG5cdFx0XHRcdFx0JHBhcmVudC5hZGRDbGFzcyAncGFuZWwtZWxlbWVudC1oZWFydGVkJ1xuXHRcdFx0XHRcdHRvZ2dsZUVsZW1lbnQgJHBhcmVudCwgJ2Nsb3NlJ1xuXG5cdFx0ZWxzZSBpZiAkKEApLmhhc0NsYXNzICdidG4taGlkZSdcblx0XHRcdHRvZ2dsZUVsZW1lbnQgJHBhcmVudCwgJ2Nsb3NlJ1xuXHRcdFx0JHBhcmVudC5kZWxheSgyMDApLmZhZGVPdXQoMzAwKVxuXG5cdFx0ZWxzZSBpZiAkKEApLmhhc0NsYXNzICdidG4tbW9yZSdcblx0XHRcdGlmIG5vdCBoYW1tZXJ0aW1lXG5cdFx0XHRcdHRvZ2dsZUVsZW1lbnQgJHBhcmVudFxuXG5cdGlmICQod2luZG93KS53aWR0aCgpIDwgODAwXG5cblx0XHQjIE1vYmlsZSBzd2lwaW5nIHdpdGggSGFtbWVyLmpzXG5cdFx0IyBodHRwczovL2hhbW1lcmpzLmdpdGh1Yi5pb1xuXHRcdGhhbW1lcnRpbWUgPSAkKCcucGFuZWwtZWxlbWVudCAuZWxlbWVudC1jb250ZW50JykuaGFtbWVyKClcblxuXHRcdGhhbW1lcnRpbWUub24gJ3N3aXBlbGVmdCBzd2lwZXJpZ2h0IHRhcCcsIChlKSAtPlxuXG5cdFx0XHQkcGFyZW50ID0gJChlLmN1cnJlbnRUYXJnZXQpLnBhcmVudCgpXG5cblx0XHRcdGlmIGUudHlwZSBpcyAndGFwJ1xuXHRcdFx0XHR0b2dnbGVFbGVtZW50ICRwYXJlbnRcblxuXHRcdFx0ZWxzZSBpZiBlLnR5cGUgaXMgJ3N3aXBlbGVmdCdcblxuXHRcdFx0XHRpZiBub3QgJHBhcmVudC5oYXNDbGFzcyAncGFuZWwtZWxlbWVudC1vcGVuJ1xuXHRcdFx0XHRcdHRvZ2dsZUVsZW1lbnQgJHBhcmVudCwgJ29wZW4nXG5cdFx0XHRlbHNlXG5cblx0XHRcdFx0aWYgJHBhcmVudC5oYXNDbGFzcyAncGFuZWwtZWxlbWVudC1vcGVuJ1xuXHRcdFx0XHRcdHRvZ2dsZUVsZW1lbnQgJHBhcmVudCwgJ2Nsb3NlJyJdfQ==
  //# sourceURL=coffeescript

