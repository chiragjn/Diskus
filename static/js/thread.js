$(document).ready(function() {
    if($('#summernote')) {
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
            focus: false,                 // set focus to editable area after initializing summernote
        });
    }

	$('#scrollToPostReply').click(function(){
		var target = $('.post-reply-row');
		$('html,body').animate({
          scrollTop: target.offset().top
        }, 1000);
	}); 

	$('.note-image-btn').removeClass('btn-primary');
	$('.note-image-btn').addClass('btn-black');
	$('[data-toggle="tooltip"]').tooltip();
});
