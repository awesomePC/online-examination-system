jQuery_3_6_0(document).ready(function(){

    const $submit_btn = jQuery_3_6_0('#submit-btn');
    const $timer = jQuery_3_6_0('#timer');
    const duration = $timer.attr('data-duration');
    const timestamp = $timer.attr('data-timestamp');

    function update_timer(){
        const now = Date.now();
        const diff = timestamp - now;

        const sec = Math.floor((diff/1000) % 60);
        const min = Math.floor((diff/(1000 *60)) % 60);
        const hr = Math.floor((diff/(1000 *60 *60)) % 24);

        const sec_text = sec < 10 ? `0${sec}` : sec;
        const min_text = min < 10 ? `0${min}` : min;
        const hr_text = hr < 10 ? `0${hr}` : hr;

        if (diff <= 0){
            //clearInterval(handle);
            $submit_btn.click();
            return;
        }
        else if (diff <= duration/100 *10){
            $timer.addClass('badge-danger');
        }
        else if (diff <= duration/100 *30){
            $timer.addClass('badge-warning');
        }

        $timer.text(`${hr_text}:${min_text}:${sec_text}`);
    }

    update_timer();
    const handle = setInterval(update_timer, 1000);

});
