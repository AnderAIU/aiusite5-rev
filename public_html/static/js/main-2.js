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
              console.log(pagehead);
              $('#aiupages').append(pagecont);
          });
      },
      complete: function() {
        enReload = true;
        // preloader off
      },
  });
  return 0;
}

$(function(){
  const myOffcanvas = document.getElementById('offcanvas');
  const bsOffcanvas = new bootstrap.Offcanvas(myOffcanvas);
  // #1 вариант (события не всплывают)
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
});
/*
$( window ).resize(function() {
  const myOffcanvas = document.getElementById('offcanvas');
  const bsOffcanvas = new bootstrap.Offcanvas(myOffcanvas);
  bsOffcanvas.hide();
  $('#aiupages').empty();
  getPosts(sechrefs);
});
*/