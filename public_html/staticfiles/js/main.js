sechrefs="";
enReload=false;



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
              $('#aiuheader .h1').append(pagehead);
              $('#aiupages').append(pagecont);
              //console.log(post.deb);
          });
      },
      complete: function() {
        enReload = true;
        // preloader off
      },
  });
  return 0;
}

/* experimental reload 
function executeQuery() {
  getPosts(sechrefs);
  updateCall();
}
function updateCall(){
  setTimeout(function(){executeQuery()}, 5000);
}
*/
$(function(){
  /*
  himg = $('.aiumodern img').height();
  hmod = $('.aiumodern').height();
  wimg = $('.aiumodern img').width();
  hmod = $('.aiumodern').width();
  if (himg < hmod) {
    $('.aiumodern img').addClass('wb');
  } else {
    $('.aiumodern img').addClass('hb');
  }
  */
  const myOffcanvas = document.getElementById('offcanvas');
  const bsOffcanvas = new bootstrap.Offcanvas(myOffcanvas);
  $("button.aiumenu2").mouseenter(function() {
    bsOffcanvas.show();
    enReload = true;
  });
  $(".offcanvas").mouseleave(function(){
    enReload = false;
    bsOffcanvas.hide();
  });
  $('a.aiumenu2').click(function() {
    if(enReload) {
      enReload = false;
      bsOffcanvas.hide();
      var id = $(this).attr('href');
      id = id.replace('#', '');
      getPosts(id);
    }
  });
  $(".aiumodern a").click(function() {
    var id = $(this).attr('href');
    id = id.replace('#', '');
    getPosts(id);
    //console.log(id);
  });
  $('a.aiumenu2').mouseenter(function() {
    if(enReload){
      var id = $(this).attr('href');
      id = id.replace('#', '');
      getPosts(id);
    }
  });
  //executeQuery();
});

$("#aiupages").on('click', ".aiumodern a", function(e){
  e.preventDefault();
  var id = $(this).attr('href');
  id = id.replace('#', '');
  getPosts(id);
});
/*
$( window ).resize(function() {
  himg = $('.aiumodern img').height();
  hmod = $('.aiumodern').height();
  wimg = $('.aiumodern img').width();
  hmod = $('.aiumodern').width();
  if (himg < hmod) {
    $('.aiumodern img').removeClass('hb').addClass('wb');
  } else {
    $('.aiumodern img').removeClass('wb').addClass('hb');
  }
});
*/
/*
$( window ).resize(function() {
  const myOffcanvas = document.getElementById('offcanvas');
  const bsOffcanvas = new bootstrap.Offcanvas(myOffcanvas);
  bsOffcanvas.hide();
  $('#aiupages').empty();
  getPosts(sechrefs);
});
*/