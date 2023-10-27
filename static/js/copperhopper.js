$(document).ready(function () {
        console.log('Hi')
        $('#copperhoppermodal').modal({show:true});
        console.log('Hi')

    });

function copperhopper(){
    var pagesList = JSON.parse(document.getElementById('pagesList').textContent);
    console.log(pagesList)
    loading(true)
    initLinkHandler()
    initAccordion()

    getRandomPages(pagesList, function (pages) {
        $('.from .title').text('Vete desde: ' + pages[0].titleEs)
        $('.tracker').prepend(`<li>${pages[0].titleEs}</li>`)
        load('from', pages[0].slug)

        $('.to .title').text('Hasta: ' + pages[1].titleEs)
        $('.tracker').append(`<li>${pages[1].titleEs}</li>`)
        load('to', pages[1].slug)

        goal = pages[1].slug
     })
}

function loading (show) {
  if (show) {
    $('.loading').show()
  } else {
    $('.loading').hide()
  }
}

function track (title) {
  var $item = $('.tracker .temp')
  if ($item.length) {
    $item.first().text(title).removeClass('temp')
  } else {
    $(`<li>${title}</li> <br />`).insertBefore('.tracker li:last-child')
  }
}

function getRandomPages (pages, cb) {
      console.log(pages)
      $.each(pages, function (index, page) {
        page.slug = page.urlEs.replace('https://es.coppermind.net/wiki/', '');
        console.log(page.slug)
      });

  cb(pages);

}

function load (dest, slug) {
  loading(true)
  $.ajax({
  	url: 'https://es.coppermind.net/w/api.php?action=parse&format=json&page=' + slug,
    type: 'GET',
    dataType: 'jsonp',
    success: function(data){
      loading(false)
      data = $.parseHTML('<div>' + data.parse.text["*"] + '</div>')
      $(`.${dest} .info`).html(data)
      $(`.${dest} .info`)[0].scrollTo(0, 0)
      if (slug === goal && dest === 'from') {
        window.setTimeout(function () {
          if (confirm('¡Has ganado! Juega otra vez')) {
              window.location.reload();
            } else {}

        }, 1000)
      }
    },
    error: function(data) {
      loading(false)
      alert('Oops. Algo ha fallado. Inténtalo de nuevo')
    }
  });
}

function initLinkHandler () {
  $('body').on('click', 'a', function (e) {
    e.preventDefault()
    var url = e.target.href
    if (url) {
      var slug = getSlug(url)
      track(e.target.innerText)
      load('from', slug)
    }
  })
}

function getSlug (url) {
  var parts = url.split('/')
  return parts[parts.length - 1]
}

function initAccordion () {
  $('.to, .from .title').click(function () {
    $('.to').toggleClass('open')
  })
}