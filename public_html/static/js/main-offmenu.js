var sechrefs="";
var enReload=false;
var fmenu=false;
var geturls;
//var menuOffcanvas = document.getElementById('offcanvas');
//const bsmenuOffcanvas = new bootstrap.Offcanvas(menuOffcanvas);
//const windowInnerHeight = document.documentElement.clientHeight;

let pdf;
let canvas;
let isPageRendering;
let pageRenderingQueue = null;
let canvasContext;
let totalPages;
let currentPageNum = 1;

function geturlsto(urls) {
  geturls = urls;
}

function initEvents() {
  let prevPageBtn = document.getElementById('prev_page');
  let nextPageBtn = document.getElementById('next_page');
  let goToPage = document.getElementById('go_to_page');
  prevPageBtn.addEventListener('click', renderPreviousPage);
  nextPageBtn.addEventListener('click',renderNextPage);
}

// init when window is loaded
function initPDFRenderer(url) {
  // const url = 'test1.pdf'; // replace with your pdf location
  let option  = { url};
  pdfjsLib.getDocument(option).promise.then(pdfData => {
      totalPages = pdfData.numPages;
      let pagesCounter= document.getElementById('total_page_num');
      pagesCounter.textContent = totalPages;
      // assigning read pdfContent to global variable
      pdf = pdfData;
      renderPage(currentPageNum);
  });
}

function renderPage(pageNumToRender = 1, scale = 1) {
  isPageRendering = true;
  document.getElementById('current_page_num').textContent = pageNumToRender;
  pdf.getPage(pageNumToRender).then(page => {
      document.getElementById("loader").style.display = "none";
      const viewport = page.getViewport({scale :1});
      canvas.height = viewport.height;
      canvas.width = viewport.width;  
      let renderCtx = {canvasContext ,viewport};
      page.render(renderCtx).promise.then(()=> {
          isPageRendering = false;
          if(pageRenderingQueue !== null) { // this is to check of there is next page to be rendered in the queue
              renderPage(pageNumToRender);
              pageRenderingQueue = null; 
          }
      });        
  }); 
}

function renderPageQueue(pageNum) {
  if(pageRenderingQueue != null) {
      pageRenderingQueue = pageNum;
  } else {
      renderPage(pageNum);
  }
}

function renderNextPage(ev) {
  if(currentPageNum >= totalPages) {
      alert("Это последняя страница");
      return ;
  } 
  currentPageNum++;
  renderPageQueue(currentPageNum);
}

function renderPreviousPage(ev) {
  if(currentPageNum<=1) {
      alert("Это первая страница");
      return ;
  }
  currentPageNum--;
  renderPageQueue(currentPageNum);
}

function goToPageNum(ev) {
  let numberInput = document.getElementById('page_num');
  let pageNumber = parseInt(numberInput.value);
  if(pageNumber) {
      if(pageNumber <= totalPages && pageNumber >= 1){
          currentPageNum = pageNumber;
          numberInput.value ="";
          renderPageQueue(pageNumber);
          return ;
      }
  }
      alert("Введите номер страницы");
}

function getcsrf() {
  tmpcsrf=$('#aiupages').attr("tmp");
  return tmpcsrf;
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
//const csrftoken = getCookie('csrftoken');
const csrftoken = getcsrf();

function openDoc(fileurl) {
  info = [];
  currentPageNum = 1;
  $.ajax({
    url: '/doc/',
    type: 'post',
    headers: {'X-CSRFToken': csrftoken },
    dataType: 'json',
    data: JSON.stringify(fileurl),
    beforeSend: function() {
      $('#aiuviewer').empty();
      $('#aiuviewer').append('<p class="h5 pt-3 mt-3 text-center">Конвертация файла, ожидание загрузки</p>');
      $('#aiuviewer').append('<div class="tenor-gif-embed" data-postid="20214936" data-share-method="host" data-aspect-ratio="7.62" data-width="100%"></div> <script type="text/javascript" async src="/static/js/animate/embed.js"></script>');
    },
    success: function(response) {
      $.each(response, function(index, post) {
        $('#aiuviewer').empty();
        $('#aiuviewer').append(post.viewer);
        geturlsto(post.filesurl);
      });

    },
    complete: function() {
      // intial params
      console.log(geturls);
      isPageRendering= false;
      pageRenderingQueue = null;
      canvas = document.getElementById('pdf_canvas');
      canvasContext = canvas.getContext('2d');
      initEvents();
      initPDFRenderer(geturls);
    },
  });
}

function getMenu(name_page) {
  var result = true;
  var tmp;
  reloadSechrefs(name_page);
  $.ajax({
    url: '/get_param?name='+name_page,
    type: 'get',
    dataType: 'json',
    beforeSend: function() {
      // preloader on
    },
    success: function(response) {
        $.each(response, function(index, post) {
          tmp = post.fullmenu;
          if (tmp=='full') {
            $('#aiupages').removeClass('full');
          } else {
            $('#aiupages').addClass('full');
            //console.log('resp---0-', tmp);
          }
        });
    },
    complete: function() {
      // here
      result = tmp;
      return result;
    },
  });
}

function fullmenusite(i) {
  //console.log('call---', fmenu, '---', i);
  if (i==1) {
    fmenu = true;
  } else {
    fmenu = false;
  }
}

function reloadSechrefs(s) {
  window.sechrefs = s;
  console.log(window.sechrefs);
}

function getFiles(tagsfile) {
  info = [];
  $.ajax({
    url: '/get_files/',
    type: 'post',
    headers: {'X-CSRFToken': csrftoken },
    dataType: 'json',
    data: JSON.stringify(tagsfile),
    beforeSend: function() {
      $('#aiufiles').empty();
    },
    success: function(response) {
      $.each(response, function(index, post) {
        $('#aiufiles').append(post.files);
      });
    },
    complete: function() {
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
              pagecont = post.contenthtml;
              pagehead = post.header;
              tmp = post.fullmenu;
              reloadSechrefs(post.title);
              $('#aiuheader .h1').append(pagehead);
              $('#aiupages').append(pagecont);
              if (tmp=='full') {
                //fullmenusite(1);
                $('#aiupages').removeClass('full');
                //console.log('resp---1-', tmp);
              } else {
                //fullmenusite(0);
                $('#aiupages').addClass('full');
                //console.log('resp---0-', tmp);
              }
          });
      },
      complete: function() {
        enReload = true;
        //enReload = false;
        // preloader off
      },
  });
}

$(function(){
  $("button.aiumenu2").click(function() {
    getPosts('home');
  });
  $(".offcanvas").mouseleave(function(){
    getMenu(sechrefs);
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

$("#aiupages").on('mouseenter', ".aiunav a", function(e) {
  e.preventDefault();
  secid = $(this).parent().parent().attr('id');
  $('#' + secid + ' a').removeClass('active');
  $(this).addClass('active');
  myobj = { 'tags' : $('.aiunav a.active').map(function() {
    str = $(this).attr('href');
    return str.replace(/\*|%|#|&|\$/g, "");
  }).get(),
  'slug' : sechrefs,
  }
  console.log(JSON.stringify(myobj));
  getFiles(myobj);
});

$("#aiupages").on('click', '.aiufile__openview img', function(e) {
  e.preventDefault();
  myobj = {
    'fileurl' : $(this).parent().attr('ophref'),
    'mimefile' : $(this).parent().attr('mimefile'),
  };
  openDoc(myobj);
  $('.aiuviewer').addClass('active');
  $('#aiufiles').removeClass('col-md-10');
  $('#aiufiles').addClass('col-md-5');

});
$("#aiupages").on('click', '.aiuviewer .aiuviewer__close', function(e) {
  e.preventDefault();
  $('.aiuviewer').removeClass('active');
  $('#aiufiles').removeClass('col-md-5');
  $('#aiufiles').addClass('col-md-10');
});
/*
$("#aiupages").on('mouseleave', ".aiunav a", function(e) {
  e.preventDefault();
  console.log('leave aiunav');
  $(this).removeClass('active');
});
*/