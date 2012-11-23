  // JS utils 
    // Fancybox 
  $(document).ready(function() {
    $(".fancybox").fancybox();
    $(".fancybox").fancybox({
      padding: 0,
      closeClick: true,

      openEffect : 'elastic',
      openSpeed  : 150,

      closeEffect : 'elastic',
      closeSpeed  : 150,                       
    });

    $(".fancybox-feed").fancybox({
      maxWidth	: 1200,
      maxHeight	: 600,
      fitToView	: false,
      width		: '70%',
      height		: '70%',
      autoSize	: false,

      openEffect : 'elastic',
      openSpeed  : 150,

      closeEffect : 'elastic',
      closeSpeed  : 150,                       
      close : [27],

    });

    $(".fancybox-landing").fancybox({
      padding: 0,

      openEffect : 'elastic',
      openSpeed  : 150,

      closeEffect : 'elastic',
      closeSpeed  : 150,                       
      afterShow: function(){
        mixpanel.track("Opened landing page image");
      }
    });

    $(document).ready(function() {
      $('.fancybox-media').fancybox({
        openEffect  : 'none',
        closeEffect : 'none',
        nextClick: false,
        afterShow: function(){
          mixpanel.track("Opened Video");
        },
        helpers : {
          media : {}
        }
      });
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

  // Registration JS
  // csrf passed for AJAX 
  $.ajaxSetup({ 
       beforeSend: function(xhr, settings) {
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
           if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
               // Only send the token to relative URLs i.e. locally.
               xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
           }
       } 
  });
    $.validator.addMethod("usernameRegex", function(value, element){
      return this.optional(element) || /^[A-Za-z0-9._%-]+\s[A-Za-z0-9._%-]+$/i.test(value);
    }, "Please enter your full name");

    $.validator.addMethod("emailRegex", function(value, element){
      return this.optional(element) || /^[A-Za-z0-9._%-]+@(dartmouth|berkeley)\.edu$/i.test(value);
    }, "Please enter a Berkeley or Dartmouth email");

    $('#registrationForm').validate({
      rules: {
        "username": {
          required: true,
          usernameRegex: true,
        },
        "email": {
          emailRegex: true,
          remote: {
            url: "/validate/email_duplicates/",
            type: "post",
            data: { 
              response: function(){
                return $('#email').val();
              }
            }
          }
        }
      },
      messages: {
        "username": {
          required: "Your name is required",
          usernameRegex: "Please enter your full name"
        },
        "email": {
          required: "Your email is required",
          emailRegex: "Please enter a Berkeley or Dartmouth email",
          remote: "That email is already in use."
        }
      },
    
      errorClass: 'text-error',
      validClass: 'text-success',

      // shows for any error
      showErrors: function(errorMap, errorList){
        this.defaultShowErrors();
        if (errorList.length < 1){
          $('label.error').remove();
          return;
        }
        $.each(errorList, function(index, error){
          $(error.element).parent().parent().attr('class', 'control-group error');
        });
      },

      // changes form to green on success
      success: function(label){
        label.parent().parent().attr('class', 'control-group success');
      }
    });

  function handleDragStart(e){
    this.style.opacity = '0.4';
    this.classList.add('over');

    // set source object 
    DRAGSOURCE = this;

    e.dataTransfer.effectAllowed = 'copy'; 
    e.dataTransfer.setData('Text', this.innerHTML);
  }

  var cols = document.querySelectorAll('#uncategorized .uncatmemes img');

  // for school feed
  if (cols.length == 0 ){
    var cols = document.querySelectorAll('#school_feed_memes .schoolmemes img');
  }

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
          try{
            mixpanel.track("Dragged in Meme", {"meme": DRAGSOURCE.id, "album":this.id});
          } catch(e) {
            console.log("Dragged in Meme, {meme: "+DRAGSOURCE.id+", album:"+this.id+"}")
          }
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

  // jQuery masonry for tutorial
  $(function(){
 
    var $container = $('#tut_list');
 
    $container.imagesLoaded( function(){
      $container.masonry({
        itemSelector : '.tutmemes',
      });
    });
 
  });

  // Tutorial JS 
  $('#start_me').live('click', function(){
    try{
      mixpanel.track("Clicked LetsStart button tutorial");
    } catch(e) {
      console.log('start');
    }
    $('#top_instruction').fadeOut('medium', function(){
      $('#lower_instruction').html('Name a friend you share experiences with').attr('class', 'lead');
      $('#start_me').hide();
      $('#friend_div').fadeIn('slow');
    });
  });

  // Tutorial: enter friends name JS
  $('#friend_form').submit(function(){
    var csrftoken = getCookie('csrftoken');
    $.ajax({
      data: $(this).serialize(),
      type: "post",
      url: $(this).attr('action'),
      datatype: 'json',
      success: function(response){
        // returns json with title and id 
        try{
          mixpanel.track("Entered friend name");
        } catch(e) {
          console.log('friend name');
        }
        $('#albums_display img').attr('id',response['id']); // change id for dragging
        $('#friend_div').fadeOut('medium', function(){
          $('#logo_tutorial').hide();
          $('#lower_instruction').html('This is your Album!').attr('class', 'lead');
          $('#second_lower_instruction').fadeIn('medium', function(){
            $('#my_first_album_title').html(response['title']);
            $('#albums_display').fadeIn('slow', function(){
              $('#letsinvite').fadeIn('medium');
              $('#letsinvitehelper').fadeIn('medium');
            });
          });
        });
      }
    });
    return false;
  });

  $('#letsinvite').live('click', function(){
    try{
      mixpanel.track("Invited friend");
      console.log("invited");
    } catch(e) {
      console.log('invite friend');
    }
  });

  $('#create_album_form').submit(function(){
    try{
      mixpanel.track("Created Album");
      console.log("album created");
    } catch(e) {
      console.log('Created Album');
    }
  });

  //$('.render_image').live('click', function(){
    //$('.image_active').attr('class','image_not_active'); // change to inactive
    //$('img', this).attr('class','image_active');

    //var imgSrcVal = $('img', this).attr("src"); // grab img source
    //$('img','#main_comic').attr('src', imgSrcVal);
  //});

// Script for Recreation Nodes
$('.render_image').live('click', function(){
    $('.image_active').attr('class','image_not_active'); // change to inactive
    $('img', this).attr('class','image_active');

    var meme_active_id = $('.image_active').attr('id');
    var meme_id = $('img', this).attr('id');
    
    $.post('/recreate_map/'+meme_id+'/', {
      'meme_active_id':meme_active_id
    }, function(data){
      $('#big_container').html(data);
    });
  });
