jQuery_3_6_0(document).ready(function(){

    let $question = jQuery_3_6_0('#question');
    let $question_num = jQuery_3_6_0('#question-num');
    let $input_q_num = jQuery_3_6_0('input[name=q_num]');
    let $label_option_A = jQuery_3_6_0('label[for=option_A]');
    let $label_option_B = jQuery_3_6_0('label[for=option_B]');
    let $label_option_C = jQuery_3_6_0('label[for=option_C]');
    let $label_option_D = jQuery_3_6_0('label[for=option_D]');

    let $question_form = jQuery_3_6_0('#question-form');
    let $bookmark_form = jQuery_3_6_0('#bookmark-form')
    let $clear_form = jQuery_3_6_0('#clear-form');
    let $clear_btn = jQuery_3_6_0('#clear-btn');

    let $prev = jQuery_3_6_0('#prev');
    let $next = jQuery_3_6_0('#next');

    let $alert = jQuery_3_6_0('#alert-template .alert');
    let $alert_container = jQuery_3_6_0('#alert-container');

    let $btn_all_ques = jQuery_3_6_0('#btn-all-ques');
    let $question_list = jQuery_3_6_0('#question-list');
    let $tmpl_btn_que = jQuery_3_6_0('#template-btn-question button');

    function update_question(data){
        $question.text(data.question);
        $question_num.text(data.q_num);
        $input_q_num.attr('value', data.q_num);
        $label_option_A.text(data.option_A);
        $label_option_B.text(data.option_B);
        $label_option_C.text(data.option_C);
        $label_option_D.text(data.option_D);
        if (data.answer){
            jQuery_3_6_0(`input[name="answer"][value="${data.answer}"]`)
            .prop('checked', true);
            $clear_btn.prop('disabled', false);
        }
        else{
            $clear_btn.prop('disabled', true);
        }
    }

    function update_pagination(data){
        if (data.prev_q_num){
            $prev.attr('data-href', '?question=' + data.prev_q_num)
            .prop('disabled', false);
        }
        else{
            $prev.prop('disabled', true);
        }
        if (data.next_q_num){
            $next.attr('data-href', '?question=' + data.next_q_num)
            .prop('disabled', false);
        }
        else{
            $next.prop('disabled', true);
        }
    }

    function alert_message(color, message){
        let alert = $alert.clone().addClass('alert-' + color);
        alert.find('.alert-message').html(message);
        alert.prependTo($alert_container);
    }

    function get_question(){
        jQuery_3_6_0.ajax({
            type: 'GET',
            url: jQuery_3_6_0(this).attr('data-href'),
            success: function (data){
                $alert_container.empty();
                $question_form.trigger('reset');
                update_question(data);
                update_pagination(data);
            },
            error: function(data){
                console.error('FAILED TO GET QUESTION');
                console.error(data);
            }
        });
    }

    function ajax_submit_form(success_func){
        jQuery_3_6_0.ajax({
            type: jQuery_3_6_0(this).attr('method'),
            url: jQuery_3_6_0(this).attr('action'),
            data: jQuery_3_6_0(this).serialize(),
            success: success_func,
            error: function(data) {
                console.error('FAILED');
                console.error(data);
            }
        });
    }

    // Submit on option select
    jQuery_3_6_0('input[name="answer"]').change(function(){
        $question_form.submit();
    });

    // Submit form with ajax
    $question_form.submit(function () {
        ajax_submit_form.bind(this)(function (data) {
            if (data.status == 'ok'){
                alert_message('success', data.message);
                $clear_btn.prop('disabled', false);
            }
            else{
                alert_message('danger', data.message);
            }
        });
        return false;
    });

    $clear_form.submit(function () {
        ajax_submit_form.bind(this)(function (data) {
            if (data.status == 'ok'){
                alert_message('success', data.message);
                $question_form.trigger('reset');
                $clear_btn.prop('disabled', true);
            }
            else{
                alert_message('danger', data.message);
            }
        });
        return false;
    });

    $bookmark_form.submit(function () {
        ajax_submit_form.bind(this)(function (data) {
            if (data.status == 'ok'){
                alert_message('success', data.message);
            }
            else{
                alert_message('danger', data.message);
            }
        });
        return false;
    });

    // Pagination
    jQuery_3_6_0('#first, #last')
    .add($prev)
    .add($next)
    .click(function(){
        get_question.bind(this)();
    });

    // Modal links
    jQuery_3_6_0('.q-links').click(function(){
        get_question.bind(this)();
        $btn_all_ques.click();
        return false;
    });

    // Get all questions
    $btn_all_ques.click(function(){
        jQuery_3_6_0.ajax({
            type: 'GET',
            url: jQuery_3_6_0(this).attr('data-href'),
            success: function (data){
                $question_list.empty();
                data.questions.forEach((que, i) => {
                    q_num = i+1
                    let link_question = $tmpl_btn_que
                    .clone(true)
                    .text(q_num + '. ' + que.answer)
                    .attr('data-href', '?question='+q_num);
                    if (que.bookmark){
                        link_question.addClass('list-group-item-warning');
                    }
                    $question_list.append(link_question);
                });
            },
            error: function(data){
                console.error('FAILED TO GET QUESTIONS');
                console.error(data);
            }
        });
    });

    // Get initial question
    jQuery_3_6_0('#first').click();
});
