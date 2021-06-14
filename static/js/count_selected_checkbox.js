jQuery_3_6_0(document).ready(function(){
    const $select_counter = jQuery_3_6_0("#select-counter");
    jQuery_3_6_0(".checkbox").change(function(){
        $select_counter.text(jQuery_3_6_0(".checkbox:checked").length);
    });
});
