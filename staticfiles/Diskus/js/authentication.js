/**
 * Created by paren on 9/16/2015.
 */
function email_check (email) {
    var re = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    return re.test(email);
}

function pass_check (password) {
    var error = "Your password must ";
    var e = 0;
    if(password.length < 8){
        if(e==0 || e==1) {
            error += "be at least 8 characters long";
            e = 1;
        }
    }
    if(password.search(/[a-z]/i)<0){
        if(e==0){
            error += "contain at least one alphabet";
            e = 2;
        }
        else{
            error += ", contain at least one alphabet";
            e = 3;
        }
    }
    if(password.search(/[0-9]/)<0){
        if(e==0){
            error += "contain at least one digit";
        }
        else if(e==1){
            error += ", contain at least one digit";
        }
        else if(e==2||e==3){
            error += "and one digit";
        }
    }
    if(e==0){
        return 0;
    }
    else{
        return error;
    }
}

function dob_check (dob) {
    return /^\d\d\/\d\d\/\d\d\d\d$/.test(dob);
}

function phone_check (phone) {
    return /^[0-9]{10}$/.test(phone);
}

function name_check (name) {
    var re = /^[a-zA-Z]+$/;
    return (re.test(name));
}

function bio_check (bio) {
    return /^.{10,500}$/.test(bio);
}

function username_check (username){
    return /^[0-9a-zA-Z_]+$/.test(username);
}