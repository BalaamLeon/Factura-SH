//$('.question-form').each(function(){
//    var this_id = $(this).attr('id');
//    var this_form = document.getElementById(this_id);
//    var question_id = this_id.split('-')[0];
//
//    var message_input = this_form.getElementsByClassName('answer-text-input')[0];
//    message_input.setAttribute("style", "height:" + (message_input.scrollHeight) + "px;overflow-y:hidden;");
//    message_input.addEventListener("input", OnInput, false);
//
//    function OnInput() {
//        var char_count = message_input.value.length;
//        var count_div = this_form.getElementsByClassName('characters-left')[0];
//        count_div.innerHTML = char_count + "/2000";
//        message_input.style.height = "auto";
//        message_input.style.height = (message_input.scrollHeight) + "px";
//    }
//    OnInput();
//
//    var answer_select = this_form.getElementById('answers')
//    var new_answer_key = this_form.getElementById('new_key')
//    answer_select.addEventListener("change", function(){
//        switch(answer_select.selectedIndex){
//            case 0:
//                message_input.value = '';
//                new_answer_key.style.display = "none";
//                break;
//            case answer_select.options.length-1:
//                new_answer_key.style.display = "block";
//                break;
//            default:
//                if(answer_select.value.includes('invoice_url')){
//                    message_input.value = answer_select.value.replace('invoice_url', answer_select.dataset.formUrl);
//                    OnInput();
//                } else {
//                    message_input.value = answer_select.value;
//                }
//                OnInput();
//                new_answer_key.style.display = "none";
//        }
//    })
//
//    function save_answer(key, message){
//        var url = '/es/sale/predefined_answer';
//        $.ajax({
//            type:'POST',
//            url:url,
//            data:{
//                key:key,
//                message:message,
//                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
//                action: 'post'
//            },
//            success:function(json){
//                console.log('Answer saved')
//            },
//            error : function(xhr,errmsg,err) {
//                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
//            }
//        });
//    }
//
//    this_form.on("submit", function (event) {
//        event.preventDefault();
//        if (message_input.value !== ''){
//            var message = message_input.value
//            if(answer_select.value == 'new'){
//                var key = new_answer_key.value;
//                save_answer(key, message)
//            }
//
//            var form_url = $(this).data('form-url');
//
//            $.ajax({
//                type:'POST',
//                url:form_url,
//                data:{
//                    pack_id:$('#pack_id').val(),
//                    buyer_id:$('#buyer_id').val(),
//                    message:message,
//                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
//                    action: 'post'
//                },
//                success:function(json){
//                    if(json.response === 201){
//                        this_form.getElementById("message-form").reset();
//                        $(".direct-chat-messages").prepend('<div class="direct-chat-msg right">'+
//                            '<img class="direct-chat-img" src="{% static "img/logo.jpg" %}" alt="message user image">' +
//                            '<div class="direct-chat-text" style="background-color: #007bff; border-color: #007bff; color: #fff; float: right; margin-right: 10px !important;">' +
//                                json.message +
//                            '</div>' +
//                            '<div class="direct-chat-infos clearfix" style="padding: 0 50px 0 50px; clear: right;">' +
//                                '<span class="direct-chat-timestamp float-right">' + json.time + '</span>' +
//                            '</div>' +
//                        '</div>'
//                        )
//                    } else {
//                        toastr.error('Ocurrió un error. El mensaje no se envió.');
//                    }
//                },
//                error : function(xhr,errmsg,err) {
//                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
//                }
//            });
//        }
//    });
//});


//
//
$('.answer-text-input').on('keyup', function(){
    OnInput($(this));
});

function OnInput(input) {
    const text = input.val();
    const lines = text.split("\n");
    const lines_count = lines.length;

    var char_count = text.length;
    var count_div = input.parent().find('.characters-left');
    count_div.text(char_count + "/2000");
    if(lines_count > 1){
        input.css('height', "auto");
        input.css('height', (input.prop("scrollHeight") + 2) + "px");
    }
}


$('.answers-select').on('change', function(){
    var message_input = $(this).parent().parent().parent().find('.answer-text-input');
    var new_answer_key = $(this).parent().parent().find('.new_key');
    switch($(this).prop('selectedIndex')){
        case 0:
            message_input.val('');
            new_answer_key.hide();
            break;
        case $(this).children('option').length-1:
            new_answer_key.show();
            break;
        default:
            if($(this).val().includes('invoice_url')){
                message_input.val($(this).val().replace('invoice_url', $(this).dataset.formUrl));
                OnInput();
            } else {
                message_input.val($(this).val());
            }
            OnInput(message_input);
            new_answer_key.hide();
    }
})

function save_answer(key, message){
    var url = '/es/answer/predefined';
    $.ajax({
        type:'POST',
        url:url,
        data:{
            key:key,
            message:message,
            context:'q',
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success:function(json){
            toastr.success('Respuesta guardada');
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

$('.question-form').on("submit", function (event) {

    event.preventDefault();
    var this_form = $(this);
    var message_input = this_form.find('.answer-text-input');
    if (message_input.val() !== ''){
        var message = message_input.val()
        var answer_select = this_form.find('.answers-select');
        if(answer_select.val() == 'new'){
            var new_answer_key = this_form.find('.new_key');
            var key = new_answer_key.val();
            save_answer(key, message)
        }

        var form_url = this_form.data('form-url');
        var question_id = this_form.find('.question-id').val();

        $.ajax({
            type:'POST',
            url:form_url,
            data:{
                question_id:question_id,
                message:message,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success:function(json){
                if(json.response === 201){
                    toastr.success('Respuesta enviada');
                    this_form.parent().parent().parent().parent().parent().parent().hide();
                } else {
                    toastr.error('Ocurrió un error. La respuesta no se envió.');
                }
            },
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }
});