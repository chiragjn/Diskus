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
        var $date = $('#date');
        var $bio = $('#bio');
        var $loc = $('#loc');
        var fname = false;
        var lname = false;
        var date = false;
        var bio = false;
        var loc =  false;

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
        if(fname && lname && date && bio && loc){
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
