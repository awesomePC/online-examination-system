jQuery_3_6_0(document).ready(function(){
    const $search_table = jQuery_3_6_0("#search-table tr");
    jQuery_3_6_0("#search-input").on("keyup", function(){
        const value = jQuery_3_6_0(this).val().toLowerCase();
        $search_table.filter(function(){
            jQuery_3_6_0(this)
            .toggle(jQuery_3_6_0(this).text().toLowerCase().indexOf(value) > -1);
        });
    });
});
