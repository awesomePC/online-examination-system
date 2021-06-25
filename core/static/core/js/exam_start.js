jQuery_3_6_0(document).ready(function(){

    const $question = jQuery_3_6_0('#question');
    const $question_num = jQuery_3_6_0('#question-num');
    const $input_q_num = jQuery_3_6_0('input[name=q_num]');
    const $label_option_A = jQuery_3_6_0('label[for=option_A]');
    const $label_option_B = jQuery_3_6_0('label[for=option_B]');
    const $label_option_C = jQuery_3_6_0('label[for=option_C]');
    const $label_option_D = jQuery_3_6_0('label[for=option_D]');
    const $marks_on_correct_answer = jQuery_3_6_0('#marks-on-correct-answer');
    const $marks_on_wrong_answer = jQuery_3_6_0('#marks-on-wrong-answer');

    const $question_form = jQuery_3_6_0('#question-form');
    const $bookmark_form = jQuery_3_6_0('#bookmark-form')
    const $clear_form = jQuery_3_6_0('#clear-form');
    const $clear_btn = jQuery_3_6_0('#clear-btn');

    const $prev = jQuery_3_6_0('#prev');
    const $next = jQuery_3_6_0('#next');

    const $alert = jQuery_3_6_0('#alert-template .alert');
    const $alert_container = jQuery_3_6_0('#alert-container');

    const $btn_all_ques = jQuery_3_6_0('#btn-all-ques');
    const $question_list = jQuery_3_6_0('#question-list');
    const $tmpl_btn_que = jQuery_3_6_0('#template-btn-question button');

    function linebreaksbr(element, text){
        element.empty()
        const lines = text.split('\n');
        lines.forEach(line => {
            element.append(document.createTextNode(line));
            element.append('<br>');
        });
    }

    function update_question(data){
        linebreaksbr($question, data.question);
        $question_num.text(data.q_num);
        $input_q_num.attr('value', data.q_num);
        $label_option_A.text('A) ' + data.option_A);
        $label_option_B.text('B) ' + data.option_B);
        $label_option_C.text('C) ' + data.option_C);
        $label_option_D.text('D) ' + data.option_D);
        $marks_on_correct_answer.text(data.marks_on_correct_answer);
        $marks_on_wrong_answer.text(data.marks_on_wrong_answer);
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
        const alert = $alert.clone().addClass('alert-' + color);
        alert.find('.alert-message').html(message);
        $alert_container.empty().append(alert);
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
                    const link_question = $tmpl_btn_que
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
