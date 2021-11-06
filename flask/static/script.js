const load_button = document.querySelector('#load-button');
var current_mood;
let gifs_increment = 12;
var show_text_gifs = true;

function GifClickFunction(gif_link) {
  navigator.clipboard.writeText(gif_link); 
  $( "#alert-popup" ).stop(true, false).fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
};

// GIFs are shown or hidden by setting the display class 
// based on whether each GIF illustrates the specified mood
$(document).ready(function() {
  $(".mood-button").click(function() {
    current_mood = this.id;
    clear_gifs();
    refresh_gifs(gifs_to_load=gifs_increment);
  });

  $("#textToggler").change(function() {
    show_text_gifs = !show_text_gifs;
    clear_gifs();
    refresh_gifs(gifs_to_load=gifs_increment);
  });
  $("#textToggler").prop('checked', true).change();


  $("#load-button").click(function() {
    refresh_gifs(gifs_to_load=gifs_increment);
  });

  current_mood = 'All';
  $(".mood-button").filter(`[id=${current_mood}]`).trigger("click");
});

// Make back to top button only visibile after scrolling
$(document).scroll(function() {
  var y = $(this).scrollTop();
  var height_banner = $(".banner").height();
  var height_settings = $(".settings").height();
  if (y > height_banner + height_settings) {
    $('.back-to-top').addClass("show")
    $('.back-to-top').removeClass("hide")
  } else {
    $('.back-to-top').addClass("hide");
    $('.back-to-top').removeClass("show")
  }
});


function set_visibility(item, visible=True, class_visible='d-flex', class_invisible='d-none') {
  if (visible) {
    item.addClass(class_visible);
    item.removeClass(class_invisible);
  } else {
    item.addClass(class_invisible);
    item.removeClass(class_visible);
  }
}

function clear_gifs() {
  $('.gif').each(function(i, obj) {
    set_visibility($(obj).parent(), visible=false);
  });
};

function refresh_gifs(gifs_to_load) {
  still_gifs_to_load = false;
  gifs_loaded = 0;
  $('.gif').each(function(i, obj) {
        moods = $(obj).attr("data-moods")
        has_text = $(obj).attr("data-hasText")
        // Always show gifs with no text
        // Only show gifs with text if this has been set
        let show_gif = has_text == 0 || !(has_text == 1 && !show_text_gifs);
        let visible = ($(obj).parent().hasClass("d-flex"))
        let displays_mood = moods.indexOf(current_mood) >= 0;
        
        if (!visible && displays_mood && gifs_loaded < gifs_to_load && show_gif) {
          set_visibility($(obj).parent(), visible=true)
          gifs_loaded++;
        } else if (!displays_mood || !show_gif) {
          set_visibility($(obj).parent(), visible=false)
        }

        if (displays_mood && show_gif && gifs_loaded == gifs_to_load) {
          set_visibility($(load_button), visible=true, class_visible='d-inline');
          return false; // break
        } else {
          set_visibility($(load_button), visible=false, class_visible='d-inline');
        }
    });
};