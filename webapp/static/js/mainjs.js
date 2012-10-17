  // JS utils #}
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
  // end #}

  function handleDragStart(e){
    this.style.opacity = '0.4';
    this.classList.add('over');

    // set source object #}
    DRAGSOURCE = this;

    e.dataTransfer.effectAllowed = 'copy'; 
    e.dataTransfer.setData('Text', this.innerHTML);
  }

  var cols = document.querySelectorAll('#uncategorized .uncatmemes');
  [].forEach.call(cols, function(col) {
    col.addEventListener('dragstart', handleDragStart, false);
  });

  var bin = document.querySelectorAll('.experiences_list');

  // when image dragged over album #}
  addEvent(bin, 'dragover', function(e){
    if (e.preventDefault)
      e.preventDefault();

    e.dataTransfer.dropEffect = 'copy';
    return false;
  });

  // when image dropped into album #}
  addEvent(bin, 'drop', function(e) {
    if (e.stopPropagation)
      e.stopPropagation();

    // link specific meme to disappear #}
    if (DRAGSOURCE){
      $(DRAGSOURCE).remove(); 
    
      var csrftoken = getCookie('csrftoken');

      // AJAX call to add meme into album - server side #}
      $.post('/meme_in_album/', {
        
        // figure out better way to retrieve id
        meme:DRAGSOURCE.id,
        album:this.id,
        'csrfmiddlewaretoken': csrftoken  
      }, 
        function(data){
          console.log(data);
      });
    }
  });
