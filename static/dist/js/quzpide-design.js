var images_ul = document.getElementById('p_images')
var images = document.getElementsByName('p_image')
var fileList = [];
var fileNames = [];

var add_img_btn = document.getElementById("add_img_btn");
add_img_btn.addEventListener('change', handleFiles);

function handleFiles() {
    if (this.files.length + fileList.length > 10) {
        alert("You can select max 10 images");
    } else {
        for (var i = 0; i < this.files.length; i++) {
            if (fileNames.indexOf(this.files[i].name) === -1) {
                fileList.push(this.files[i]);
                fileNames.push(this.files[i].name);

                var li_li = document.createElement("li");
                var img_i = fileList.length - 1
                li_li.setAttribute("id", "image_" + img_i);

                var li = document.createElement("div");
                li.setAttribute("class", "list");

                var img = document.createElement("img");
                if(this.files[i].type == "application/pdf"){
                    img.setAttribute("src", "/static/img/pdf-placeholder.png");
                } else{
                    img.setAttribute("src", URL.createObjectURL(this.files[i]));
                }
                img.setAttribute("name", "p_image");
                img.setAttribute("id", this.files[i].name);
                img.setAttribute("style", "left: 0px")
                li.appendChild(img);

                var title = document.createElement("span");
                title.innerHTML = this.files[i].name;
                li.appendChild(title);

                var remove_div = document.createElement("div");
                remove_div.setAttribute("class", "remove_img_div");

                var remove_btn = document.createElement("button");
                remove_btn.setAttribute("type", "button")
                remove_btn.setAttribute("class", "btn btn-secondary remove_img")
                remove_btn.setAttribute("id", "remove_" + i)
                remove_btn.setAttribute("onClick", "remove_img(this.id)")
                remove_btn.innerHTML = '<i class="fas fa-trash" />';
                remove_div.appendChild(remove_btn);
                li.appendChild(remove_div);
                li_li.appendChild(li);
                images_ul.appendChild(li_li);

            } else {
                alert(this.files[i].name + " already selected")
            }
        }
    }
    console.log(fileList);
}
function remove_img(clicked_id){
    var id = clicked_id.split('_')[1]
    fileList.splice(id, 1);
    fileNames.splice(id, 1);
    var d = document.getElementById("p_images");
    var d_nested = document.getElementById("image_" + id);
    var throwawayNode = d.removeChild(d_nested);
};

var submited = false
$('#design_form').on('submit', function(e) {
//    alert('Handler for .submit() called.');
    e.preventDefault();
    e.returnValue = false;
    $('#submitBtn').prop('disabled', true)
    if(submited == false){
        if(fileList.length > 0){
           save_images($('#id_meli_sale').val(), this)
        }
    } else {
        window.location.replace("/es/quzpide/success");
    }
//    $(this).submit();
//    return true; // return false to cancel form action
});

function save_images(album_id, form){
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var image_create_url = $('#design_form').data('image-create-url');
    var images_saved = 0;

    for (var i = 0; i < fileList.length; i++) {
        var data = new FormData();
        var file = fileList[fileNames.indexOf(images[i].id)];

        data.append('image', file);
        data.append('image_name', images[i].id);
        data.append('album_id', album_id);
        data.append('image_position', i);

        function imgCallback(response) {
            images_saved += 1;
            if(images_saved == fileList.length){
                submited = true
                $(form).submit();
            }
        }


        $.ajax({
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function(evt) {
                    if (evt.lengthComputable) {
                        var percentComplete = evt.loaded / evt.total;
                        var progress_bar = $('#progress-bar')
                        progress_bar.css('width', percentComplete + '%')
                        progress_bar.attr('aria-valuenow', percentComplete)
                        progress_bar.html(percentComplete + '%')
                        //Do something with upload progress here
                    }
               }, false);

               xhr.addEventListener("progress", function(evt) {
                   if (evt.lengthComputable) {
                       var percentComplete = evt.loaded / evt.total;
                       //Do something with download progress
                   }
               }, false);

               return xhr;
            },
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            type : 'POST',
            cache: false,
            processData: false,
            contentType: false,
            url :  image_create_url,
            data : data,
            success : imgCallback,
            error: function(data) {
              alert("Something Went Wrong");
            }
        });
    };
}
