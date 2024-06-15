(function($) {
    "use strict";

    window.confirmReactivar = function(userId) {
        swal({
            title: "¿Estás seguro?",
            text: "¿Deseas reactivar este usuario?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then((willReactivate) => {
            if (willReactivate) {
                window.location.href = "/usuarios/" + userId + "/reactivar/";
            }
        });
    };

    window.confirmDelete = function(userId) {
        swal({
            title: "¿Estás seguro?",
            text: "Una vez eliminado, no podrás recuperar este usuario.",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then((willDelete) => {
            if (willDelete) {
                window.location.href = "/usuarios/" + userId + "/eliminar/";
            }
        });
    };

    window.confirmSubmit = function(formId, message) {
        swal({
            title: "¿Está seguro?",
            text: message,
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then((willSubmit) => {
            if (willSubmit) {
                document.getElementById(formId).submit();
            }
        });
    };

})(jQuery);