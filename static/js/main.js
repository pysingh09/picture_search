const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

$("#search_picture").submit(function(e){
    e.preventDefault();
    getPicture();
});

function getPicture(){
    var latitude = $('#lat').val();
    var longitude = $('#log').val();
    var page = $('#page_count').val();
    $.ajax({
      type: "POST",
      headers: { "X-CSRFToken": csrftoken },
      url: "/flicker-images/",
      data: {
        latitude: latitude,
        longitude: longitude,
        page: page,
      },
      success: function(data){
        $('#search_result').html('');
        var obj = data.records['photos']
        if(obj['photo'].length > 0){
            $.each( obj['photo'], function( key, value ) {
              $('#search_result').append("<div class='img_wrp'><img src="+value.url_t+" class='img-thumbnail' alt='Cinque Terre'></div>")
            });
        }
        else{
            $('#search_result').append("<p> NO Record Found</p>")
        }
        if(obj.pages > obj.page){
            $("#page_count").val(obj.page+1)
            $('#search_result').append("<div class='form-group'><button onclick='getPicture()' class='btn btn-primary btn-block show_more' type='submit'>Show More Results</button></div>")
        }
      },
      error: function (error) {
        console.log(error)
      },
      dataType: "json"
    });
}

$('select[name="locations"]').change(function(){
    var latitude = $(this).val().split(",")[0]
    var longitude = $(this).val().split(",")[1]
    $('#lat').val(latitude);
    $('#log').val(longitude);
});


function myFunction(imgs) {
  var expandImg = document.getElementById("expandedImg");
  var imgText = document.getElementById("imgtext");
  expandImg.src = imgs.src;
  imgText.innerHTML = imgs.alt;
  expandImg.parentElement.style.display = "block";
}

// external js: masonry.pkgd.js, imagesloaded.pkgd.js

// init Masonry
var grid = document.querySelector('.grid');

var msnry = new Masonry( grid, {
  itemSelector: '.grid-item',
  columnWidth: '.grid-sizer',
  percentPosition: true
});

imagesLoaded( grid ).on( 'progress', function() {
  // layout Masonry after each image loads
  msnry.layout();
});
