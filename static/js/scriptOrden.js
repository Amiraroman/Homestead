
function editarOrden(id_orden, fecha, estado, id_cliente) {
    document.getElementById('editarIdOrden').value = id_orden;
    document.getElementById('editarFecha').value = fecha;
    document.getElementById('editarEstado').value = estado;
    document.getElementById('editarIdCliente').value = id_cliente;

    var editarOrdenForm = document.getElementById('editarOrdenForm');
    editarOrdenForm.action = '/orden/editar/' + id_orden;

    var myModal = new bootstrap.Modal(document.getElementById('modalEditarOrden'), {
        keyboard: false
    });
    myModal.show();
}

