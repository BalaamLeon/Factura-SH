var this_js_script = $('script[src*=list_page]'); // or better regexp to get the file name..
var object = this_js_script.attr('data-object');

var add_formURL = $('#create-btn').data('form-url');
var import_formUrl = $('#import-btn').data('form-url');

$(function () {

    // Import Objects asynchronous button
    // message
    var asyncSuccessMessageCreate = [
            "<script>",
            "    toastr.success('Success: " + object + "s imported correctly.');",
            "</script>"
        ].join("");

    function importAsyncModalForm() {
        if ($('#import-btn').length>0) {
            // modal form
            $("#import-btn").modalForm({
                formURL: import_formUrl,
                modalID: "#modal",
                asyncUpdate: true,
                errorClass: ".invalid-feedback",
                asyncSettings: {
                  closeOnSubmit: true,
                  successMessage: asyncSuccessMessageCreate,
                  dataUrl: "list_table",
                  dataElementId: "#list_table",
                  dataKey: "table",
                  addModalFormFunction: reinstantiateModalForms
                }
            });
        }
    }
    importAsyncModalForm();

    // Create object asynchronous button
    // message
    var asyncSuccessMessageCreate = [
        "<script>",
        "    toastr.success('Success: " + object + " was created.');",
        "</script>"
    ].join("");

    // modal form
    function createAsyncModalForm() {
        $("#create-btn").modalForm({
            formURL: add_formURL,
            modalID: "#modal",
            asyncUpdate: true,
            errorClass: ".invalid-feedback",
            asyncSettings: {
                closeOnSubmit: true,
                successMessage: asyncSuccessMessageCreate,
                dataUrl: "list_table",
                dataElementId: "#list_table",
                dataKey: "table",
                addModalFormFunction: reinstantiateModalForms
            }
        });
    }
    createAsyncModalForm();

    // Update object asynchronous button
    // message
    var asyncSuccessMessageUpdate = [
        "<script>",
        "    toastr.success('Success: " + object + " was updated.');",
        "</script>"
    ].join("");

    // modal form
    function updateModalForm() {
        $(".update-btn").each(function () {
            $(this).modalForm({
                formURL: $(this).data("form-url"),
                asyncUpdate: true,
                errorClass: ".invalid-feedback",
                asyncSettings: {
                    closeOnSubmit: true,
                    successMessage: asyncSuccessMessageUpdate,
                    dataUrl: "list_table",
                    dataElementId: "#list_table",
                    dataKey: "table",
                    addModalFormFunction: reinstantiateModalForms
                }
            });
        });
    }

    updateModalForm();


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

    function reinstantiateModalForms() {
        importAsyncModalForm();
        createAsyncModalForm();
        updateModalForm();
        detailModalForm();
        deleteModalForm();
    }
});

