var rfc_input = document.getElementById('id_rfc')
var name_input = document.getElementById('id_name')
var cp_input = document.getElementById('id_cp')
var regimen_input = document.getElementById('id_regimen')
rfc_input.addEventListener('focusout', (event) => {
    $.ajax({
        type:'GET',
        url:rfc_input.dataset['url'],
        data:{
            rfc:rfc_input.value,
        },
        success:function(json){
            if(json.response == 'ok'){
                name_input.value = json.name
                cp_input.value = json.cp
                regimen_input.value = json.regimen
            }
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
});
