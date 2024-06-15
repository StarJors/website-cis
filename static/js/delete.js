function confirmDelete(userId) {
    swal({
        title: "¿Estás seguro?",
        text: "Esta acción no se puede deshacer.",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
            window.location.href = "/usuarios/" + userId + "/eliminar/";
        }
    });
}



