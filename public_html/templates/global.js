var sechrefs="";
var enReload=false;
var menuOffcanvas = document.getElementById('offcanvas');
const bsmenuOffcanvas = new bootstrap.Offcanvas(menuOffcanvas);
menuOffcanvas.addEventListener('shown.bs.offcanvas', function () {
  enReload = true;
});
menuOffcanvas.addEventListener('hidden.bs.offcanvas', function () {
  enReload = false;
});

function getMenu(name_page) {
  $.ajax({
    url: '/get_param?name='+name_page,
    type: 'get',
    dataType: 'json',
    beforeSend: function() {
      // preloader on
    },
    success: function(response) {
        $.each(response, function(index, post) {
            result = post.fullmenu;
            console.log(post.title);
            console.log(result, '---', name_page);
        });
    },
    complete: function() {
      return result;
      // preloader off
    },
  });
}

function getPosts(name_page) {
  $.ajax({
      url: '/get_pages?name='+name_page,
      type: 'get',
      dataType: 'json',
      beforeSend: function() {
        enReload = false;
        sechrefs = name_page;
        $('#aiuheader .h1').empty();
        $('#aiupages').empty();
        // preloader on
      },
      success: function(response) {
          $.each(response, function(index, post) {
              var pagecont = post.contenthtml;
              pagehead = post.header;
              result = post.fullmenu;
              $('#aiuheader .h1').append(pagehead);
              $('#aiupages').append(pagecont);
          });
      },
      complete: function() {
        enReload = true;
        return result;
        // preloader off
      },
  });
}


$(function(){
  const myOffcanvas = document.getElementById('offcanvas');
  const bsOffcanvas = new bootstrap.Offcanvas(myOffcanvas);
  $("button.aiumenu2").mouseenter(function() {
    bsOffcanvas.show();
  });
  $(".offcanvas").mouseleave(function(){
    console.log('2---', !getMenu(sechrefs));
    if (!getMenu(sechrefs)) {
      bsOffcanvas.hide();
      console.log('hide menu');
    } else {
      bsOffcanvas.show();
    }
  });
  $('a.aiumenu2').click(function() {
    if (enReload) {
      var id = $(this).attr('href');
      id = id.replace('#', '');
      getPosts(id);
    }
  });
  $(".aiumodern a").click(function() {
    var id = $(this).attr('href');
    id = id.replace('#', '');
    getPosts(id);
  });
  $('a.aiumenu2').mouseenter(function() {
    if (enReload) {
      var id = $(this).attr('href');
      id = id.replace('#', '');
      getPosts(id);
    }
  });
});

$("#aiupages").on('click', ".aiumodern a", function(e){
  e.preventDefault();
  var id = $(this).attr('href');
  id = id.replace('#', '');
  getPosts(id);
});

$("#aiupages").on('click', ".aiucollapseopen", function(e){
  var id = $(this).attr('data-target');
  if (!$(id).hasClass('show')) {
    $('.aiucollapse').collapse('hide');
    $(id).collapse('show');
  } else {
    $('.aiucollapse').collapse('hide');
  }
});