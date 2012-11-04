  // JS utils #}
    // Fancybox 
  $(document).ready(function() {
    $(".fancybox").fancybox();
    $(".fancybox").fancybox({
      padding: 0,

      openEffect : 'elastic',
      openSpeed  : 150,

      closeEffect : 'elastic',
      closeSpeed  : 150,                       
    });
  });

  var addEvent = (function () {
    if (document.addEventListener) {
      return function (el, type, fn) {
        if (el && el.nodeName || el === window) {
          el.addEventListener(type, fn, false);
        } else if (el && el.length) {
          for (var i = 0; i < el.length; i++) {
            addEvent(el[i], type, fn);
          }
        }
      };
    } else {
      return function (el, type, fn) {
        if (el && el.nodeName || el === window) {
          el.attachEvent('on' + type, function () { return fn.call(el, window.event); });
        } else if (el && el.length) {
          for (var i = 0; i < el.length; i++) {
            addEvent(el[i], type, fn);
          }
        }
      };
    }
  })();

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  // end 

  function handleDragStart(e){
    this.style.opacity = '0.4';
    this.classList.add('over');

    // set source object 
    DRAGSOURCE = this;

    e.dataTransfer.effectAllowed = 'copy'; 
    e.dataTransfer.setData('Text', this.innerHTML);
  }

  var cols = document.querySelectorAll('#uncategorized .uncatmemes img');
  [].forEach.call(cols, function(col) {
    col.addEventListener('dragstart', handleDragStart, false);
  });

  // drop source
  var bin = document.querySelectorAll('.experiences_list');

  // when image dragged over album 
  addEvent(bin, 'dragover', function(e){
    if (e.preventDefault)
      e.preventDefault();

    e.dataTransfer.dropEffect = 'copy';
    return false;
  });

  // when image dropped into album 
  addEvent(bin, 'drop', function(e) {
    if (e.stopPropagation)
      e.stopPropagation();

    // link specific meme to disappear 
    if (DRAGSOURCE){
      $(DRAGSOURCE).remove(); 
    
      var csrftoken = getCookie('csrftoken');

      // AJAX call to add meme into album - server side 
      $.post('/meme_in_album/', {
        
        // figure out better way to retrieve id
          // id not passed from masonry
        meme:DRAGSOURCE.id,
        album:this.id,
        'csrfmiddlewaretoken': csrftoken  
      }, function(data){
          console.log(data);
      });
    }
  });

  // jQuery masonry for profile.html
  $(function(){
 
    var $container = $('#uncategorized');
 
    $container.imagesLoaded( function(){
      $container.masonry({
        itemSelector : '.uncatmemes',
      });
    });
 
  });

  // jQuery masonry for experience_display.html
  $(function(){
 
    var $container = $('#album_list');
 
    $container.imagesLoaded( function(){
      $container.masonry({
        itemSelector : '.uncatmemes'
      });
    });
 
  });

  // Tutorial JS 
  $('#start_me').live('click', function(){
    $('#top_instruction').fadeOut('medium', function(){
      $('#lower_instruction').html('Name a friend you share experiences with');
      $('#start_me').hide();
      $('#friend_div').fadeIn('slow');
    });
  });

  // Tutorial: enter friends name JS
  $('#friend_form').submit(function(){
    //e.preventDefault();
    //return false;
    var csrftoken = getCookie('csrftoken');
    //$.post('/welcome/hello-world/create', {
    $.ajax({
      data: $(this).serialize(),
      type: "post",
      url: $(this).attr('action'),
      //'csrfmiddlewaretoken': csrftoken
      success: function(response){
        $('#friend_div').fadeOut('medium', function(){
          $('#lower_instruction').html('This is your Album!').attr('class', 'lead');
          $('#second_lower_instruction').fadeIn('medium', function(){
            $('#my_first_album_title').html(response);
            $('#albums_display').fadeIn('slow', function(){
              $('#letscreate').fadeIn('medium');
            });
          });
        });
      }
    });
    return false;
  });

  // Tutorial: create flash meme in generator
  //$('#letsflash').live('click', function(){
    //$('#lower_instruction').fadeOut('medium', function(){
      //$('#top_instruction').html('Lets create a meme for your album');
      //$('#letscreate').hide();
      ////$('#macromeme').fadeIn('slow');
      //$('#macromeme').show();
    //});
  //});


