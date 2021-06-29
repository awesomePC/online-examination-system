jQuery_3_6_0(document).ready(function(){
    jQuery_3_6_0('.confirm-form-submit').submit(function(){
        return confirm(jQuery_3_6_0(this).attr('data-confirm-msg'));
    });
});
