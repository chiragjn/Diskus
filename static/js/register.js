/**
 * Created by paren on 10/23/2015.
 */
$(document).ready(function(){
    $('#date').datepicker({
        format: 'dd/mm/yy',
        autoclose: true
    });
    $('[data-toggle="tooltip"]').tooltip();
    $('.input').keyup(function(){
        var $fname = $('#fname');
        var $lname = $('#lname');
        var $email = $('#email');
        var $username = $('#username');
        var $pass = $('#pass');
        var $cpass = $('#cpass');
        var $date = $('#date');
        var $bio = $('#bio');
        var $loc = $('#loc');
        var fname = false;
        var lname = false;
        var email = false;
        var username = false;
        var pass = false;
        var cpass = false;
        var date = false;
        var bio = false;
        var loc =  false;

        if($email.val()) {
            if(email_check($email.val())){
                email = true;
                $email.tooltip('destroy');
            }
        }
        if($pass.val()) {
            var error = pass_check($pass.val());
            if(error ==0){
                pass = true;
                $pass.tooltip('destroy');
            }
        }
        if($cpass.val()) {
            cpass = $cpass.val() == $pass.val();
            if(cpass) {
                cpass = true;
                $cpass.tooltip('destroy')
            }
        }
        if($fname.val()) {
           if(name_check($fname.val())){
                fname = true;
                $fname.tooltip('destroy');
            }
        }
        if($lname.val()) {
            if(name_check($lname.val())){
                lname = true;
                $lname.tooltip('destroy');
            }
        }
        if($loc.val()){
            if(name_check($loc.val())){
                loc = true;
                $loc.tooltip('destroy');
                console.log("dob done");
            }
        }
        if($bio.val()){
           if(bio_check($bio.val())){
                $bio.tooltip('destroy');
                bio = true;
           }
        }
        if($date.val()){
            date = true;
        }
        if($username.val()){
            if(username_check($username.val())){
                $username.tooltip('destroy');
                username = true;
            }
        }

        if(fname && lname && email && username && pass && cpass && date && bio && loc){
            console.log("all done");
            $('#submit').removeClass('disabled').attr('disabled', false);
        }
        else {
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
        if($this.attr('id') == "cpass") {
            if($this.val() != $('#pass').val()){
                has_error = true;
                error = "Passwords Don't Match";
            }
        }
        if($this.attr('id') == "username") {
            if(!username_check($this.val())) {
                has_error = true;
                error = "Username must contain only alphabets, numbers and _"
            }
        }
        if($this.attr('id') == "email") {
            if(!email_check($this.val())) {
                has_error = true;
                error = "Please Enter Valid Email";
            }
        }
        if($this.attr('id') == "fname" || $this.attr('id') == "lname" || $this.attr('id') == "loc") {
            if(!name_check($this.val())) {
                has_error = true;
                error = "Please Enter Valid Detail";
            }
        }

        if(has_error) {
            $this.attr('title', error).tooltip('fixTitle').tooltip('show');
        }

    });

});
