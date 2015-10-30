/**
 * Created by paren on 10/23/2015.
 */
/**
 * Created by paren on 10/23/2015.
 */
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    $('.input').keyup(function(){
        var $username = $('#username');
        var $pass = $('#pass');
        var username = false;
        var pass = false;
        if($pass.val()) {
            var error = pass_check($pass.val());
            if (error == 0) {
                pass = true;
                $pass.tooltip('destroy');
            }
        }
        if($username.val()){
            if(username_check($username.val())){
                $username.tooltip('destroy');
                username = true;
            }
        }

        if(username && pass){
            console.log("all done");
            $('#submit').removeClass('disabled').attr('disabled', false);
        }
        else{
            $('#submit').addClass('disabled').attr('disabled', true);
        }

    });
    $('.input').change(function(e){
        var $this = $(this);
        var has_error = false;
        var error = "";
        if($this.attr('id') == "pass") {
            error = pass_check($this.val());
            if(error != 0)
                has_error = true;
        }
        if($this.attr('id') == "username") {
            if(!username_check($this.val())) {
                has_error = true;
                error = "Username must contain only alphabets, numbers and _"
            }
        }
        if(has_error) {
            $this.attr('title', error).tooltip('fixTitle').tooltip('show');
        }

    });

});

