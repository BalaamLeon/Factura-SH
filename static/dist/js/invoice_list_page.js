var this_js_script = $('script[src*=invoice_list_page]'); // or better regexp to get the file name..
var object = this_js_script.attr('data-object');

$(document).ready(function(){

    function chatModal() {
        $(".chat-btn").each(function () {
            $(this).on("click", function(){
                $('#modal-chat').find('.modal-content').load($(this).data("form-url"), function () {
                    $('#modal-chat').modal("show");
                });

            });
        });
    }
    chatModal();

    $( "#modal-chat" ).on('shown.bs.modal', function(){
        var me = document.querySelector('script[src="/static/dist/js/chat.js"]');
        if(me !== null){
            me.remove();
        }
        var js = document.createElement("script");
        js.type = "text/javascript";
        js.src = '/static/dist/js/chat.js';
        document.body.appendChild(js);
    });

    function invoiceMenu() {
        $(".sc-ui-trigger-content__trigger").each(function () {
            $(this).on("click", function(){
                $(".sc-ui-trigger-content__content").not($(this)).addClass("sc-ui-trigger-content__content--hidden");
                $(".sc-ui-trigger-content__trigger").not($(this)).addClass("sc-ui-trigger-content__trigger--non-triggered");
                $(".sc-ui-trigger-content__trigger").not($(this)).removeClass("sc-ui-trigger-content__trigger--triggered");
                $(this).siblings(".sc-ui-trigger-content__content").removeClass("sc-ui-trigger-content__content--hidden");
                $(this).removeClass("sc-ui-trigger-content__trigger--non-triggered");
                $(this).addClass("sc-ui-trigger-content__trigger--triggered");
            });
        });
    }
    invoiceMenu();


    document.addEventListener('click', function handleClickOutsideBox(event) {
        const box = $('.sc-ui-trigger-content');
        if (box.find(event.target).length === 0) {
            box.children('.sc-ui-trigger-content__trigger').addClass("sc-ui-trigger-content__trigger--non-triggered");
            box.children('.sc-ui-trigger-content__trigger').removeClass("sc-ui-trigger-content__trigger--triggered");
            box.children(".sc-ui-trigger-content__content").addClass("sc-ui-trigger-content__content--hidden");
        }
    });



    var asyncSuccessMessageCreate = [
    "<script>",
    "    toastr.success('La factura ha sido enviada correctamente.');",
    "<\/script>"
    ].join("");

    function send_cfdi_modal_form(){
        btn = $("#send_cfdi_btn")
        btn.modalForm({
            modalID: "#modal",
            formURL: btn.data("bs-formurl"),
            errorClass: ".invalid-feedback",
            asyncUpdate: true,
            asyncSettings: {
                closeOnSubmit: true,
                successMessage: asyncSuccessMessageCreate,
                dataUrl: "list_table/pending",
                dataElementId: "#invoices-list",
                dataKey: "table",
                addModalFormFunction: reinstantiateModalForms
            }
        });
    };

    var detail_modal = document.getElementById('modal-lg');
    detail_modal.addEventListener('show.bs.modal', function (event) {
        send_cfdi_modal_form();
    });


    // Delete object button - formURL is retrieved from the data of the object
    function deleteModalForm() {
        $(".delete-btn").each(function () {
            $(this).modalForm({formURL: $(this).data("form-url"), isDeleteForm: true});
        });
    }
    deleteModalForm();



    // Object Detail button
    function detailModalForm() {
        $(".detail-btn").each(function () {
            $(this).modalForm({
                modalID: "#modal-lg",
                formURL: $(this).data("form-url")
            });
        });
    }
    detailModalForm();

    // Object Detail button
    function toggleTracking() {
        $(".toggle_tracking").each(function () {
            $(this).click(function() {
                $.ajax({
                    type: 'GET',
                    url: $(this).data("form-url"),
                    success: function (response) {
                        if (response.status == 'success') {
                            if(response.tracking) {
                                toastr.success('Solicitud agregada a la lista de seguimiento.');
                                $('#'+response.pk+'_toggle_tracking_btn').html('<i class="fa fa-eye-slash"></i>  Quitar seguimiento');
                            } else {
                                toastr.success('Se ha quitado el seguimiento.');
                                $('#'+response.pk+'_toggle_tracking_btn').html('<i class="fa fa-eye"></i>  Dar seguimiento');
                            }
                        } else {
                            toastr.warning('Ocurrió un error.');
                        }
                    }
                });
            });
        });
    };
    toggleTracking();

    // Update object asynchronous button
    // message
    var asyncSuccessMessageUpdate = [
        "<script>",
        "    toastr.success('Success: " + object + " was updated.');",
        "</script>"
    ].join("");

    // modal form
    function updateStatusModalForm() {
        $(".change_status").each(function () {
            $(this).modalForm({
                formURL: $(this).data("form-url"),
                asyncUpdate: true,
                errorClass: ".invalid-feedback",
                asyncUpdate: true,
                asyncSettings: {
                    closeOnSubmit: true,
                    successMessage: asyncSuccessMessageUpdate,
                    dataUrl: "list_table/pending",
                    dataElementId: "#invoices-list",
                    dataKey: "table",
                    addModalFormFunction: reinstantiateModalForms
                }
            });
        });
    }

    updateStatusModalForm();

    function reinstantiateModalForms() {
        $('#modal-lg').modal("hide");
        chatModal();
        invoiceMenu();
        detailModalForm();
        toggleTracking();
        updateStatusModalForm();
    }
});

