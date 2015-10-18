$(document).ready(function() {

    var $body = $("body");
    $(document).on({
        ajaxStart: function() { $body.addClass("loading");  },
        ajaxStop: function() { $body.removeClass("loading"); }
    });

    if($('#summernote')) {
        console.log("SummerNote Initialized");

        $('#summernote').summernote({
            height: 300,
            toolbar: [
                ['style', ['style']],
                ['font', ['bold', 'italic', 'underline', 'clear']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['height', ['height']],
                ['table', ['table']],
                ['insert', ['link', 'picture', 'video', 'hr']],
                ['view', ['fullscreen', 'codeview']]
            ],
            minHeight: null,             // set minimum height of editor
            maxHeight: null,             // set maximum height of editor
            focus: false,
            onImageUpload: function(files) {
                //console.log('image upload > > >:', files);
                sendFile(files[0]);
                //$summernote.summernote('insertNode', imgNode);
              }
        });


        function sendFile(file) {
            data = new FormData();
            data.append("upload", file);
            $.ajax({
                data: data,
                type: "POST",
                url: 'http://uploads.im/api',
                cache: false,
                contentType: false,
                processData: false,
                success: function (response) {
                    image_url = "-1";
                    if(response.status_code == 200)
                    {
                        image_url=response.data.img_url;
                    }
                    else
                    {
                        //error
                    }
                    console.log(image_url);
                    if(image_url=="-1")
                    {
                        //eroor
                    }
                    else
                    {
                        $('#summernote').summernote('editor.insertImage', image_url);
                    }

                }
            });
        }

        $('.note-image-btn,.note-video-btn').removeClass('btn-primary');
	    $('.note-image-btn,.note-video-btn').addClass('btn-black');



    }

	$('#scrollToPostReply').click(function(){
		var target = $('.post-reply-row');
		$('html,body').animate({
          scrollTop: target.offset().top
        }, 1000);
	}); 


	$('[data-toggle="tooltip"]').tooltip();


//    $('.quote-post').click(function(){
//
//    });
//
    $('.make-post').click(function(){
        var code = $('.note-editable').html();
        if(code.length > 0 && code !== '<p><br></p>')
        {
            $.ajax({
              type: "POST",
              url: "/makepost/",
              data:
              {
                  thread_id: $('.make-post').attr('data-thread'),
                  content: code,
                  csrfmiddlewaretoken: $('.make-post').attr('data-csrf'),
              },
              success: function (response) {
                if(response == "200")
                {
                    var redirect_url = window.location.href.split('?')[0] + '?page=100000';
                    console.log(redirect_url);
                    window.location.href = redirect_url;
                }
              }
            });
        }
        else
        {

        }
    });
//
//    $('.edit-post').click(function(){
//
//    });
//
//    $('.delete-post').click(function(){
//
//    });
//
//    $('.permalink-post').click(function(){
//
//    });

});
