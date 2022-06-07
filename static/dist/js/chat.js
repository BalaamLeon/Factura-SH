var message_form = document.getElementById('message-form');

var message_input = document.getElementById('message');
message_input.setAttribute("style", "height:" + (message_input.scrollHeight) + "px;overflow-y:hidden;");
message_input.addEventListener("input", OnInput, false);

function OnInput() {
    var char_count = message_input.value.length;
    var count_div = document.getElementById('characters-left');
    count_div.innerHTML = char_count + "/350";
    message_input.style.height = "auto";
    message_input.style.height = (message_input.scrollHeight) + "px";
}

//message_input.addEventListener('keyup', message_inputLengthCheck, false);
//message_input.addEventListener('keydown', message_inputLengthCheck, false);

OnInput();


var answer_select = document.getElementById('answers')
var new_answer_key = document.getElementById('new_key')
answer_select.addEventListener("change", function(){
    switch(answer_select.selectedIndex){
        case 0:
            message_input.value = '';
            new_answer_key.style.display = "none";
            break;
        case answer_select.options.length-1:
            new_answer_key.style.display = "block";
            break;
        default:
            if(answer_select.value.includes('invoice_url')){
                message_input.value = answer_select.value.replace('invoice_url', answer_select.dataset.formUrl);
                OnInput();
            } else {
                message_input.value = answer_select.value;
            }
            OnInput();
            new_answer_key.style.display = "none";
    }
})

function save_answer(key, message){
    var url = '/es/sale/predefined_answer';
    $.ajax({
        type:'POST',
        url:url,
        data:{
            key:key,
            message:message,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success:function(json){
            console.log('Answer saved')
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

$('#mark_as_read').click(function(){
    var url = $(this).data('form-url');
    $.ajax({
        type:'POST',
        url:url,
        data:{
            s_id: $('#pack_id').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success:function(json){
            if(json.status == 200){ // meaning that everyhting went ok
                toastr.success(json.message);
                document.location.reload(true);
             }
             else{
                toastr.error(json.message);
             }
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
});


$('#message-form').on("submit", function (event) {
    event.preventDefault();
    if (message_input.value !== ''){
        var message = message_input.value
        if(answer_select.value == 'new'){
            var key = new_answer_key.value;
            save_answer(key, message)
        }

        var form_url = $(this).data('form-url');

        $.ajax({
            type:'POST',
            url:form_url,
            data:{
                pack_id:$('#pack_id').val(),
                buyer_id:$('#buyer_id').val(),
                message:message,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success:function(json){
                if(json.response === 201){
                    document.getElementById("message-form").reset();
                    $(".direct-chat-messages").prepend('<div class="direct-chat-msg right">'+
                        '<img class="direct-chat-img" src="{% static 'img/logo.jpg' %}" alt="message user image">' +
                        '<div class="direct-chat-text" style="background-color: #007bff; border-color: #007bff; color: #fff; float: right; margin-right: 10px !important;">' +
                            json.message +
                        '</div>' +
                        '<div class="direct-chat-infos clearfix" style="padding: 0 50px 0 50px; clear: right;">' +
                            '<span class="direct-chat-timestamp float-right">' + json.time + '</span>' +
                        '</div>' +
                    '</div>'
                    )
                } else {
                    toastr.error('Ocurrió un error. El mensaje no se envió.');
                }
            },
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }
});