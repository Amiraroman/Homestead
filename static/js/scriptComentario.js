function editarComentario(id_comentario, fecha, comentario, id_producto, puntuacion, id_cliente) {
    document.getElementById('editarIdComentario').value = id_comentario;
    document.getElementById('editarFecha').value = fecha;
    document.getElementById('editarComentario').value = comentario;
    document.getElementById('editarIdProducto').value = id_producto;
    document.getElementById('editarPuntuacion').value = puntuacion;
    document.getElementById('editarIdCliente').value = id_cliente;

    const form = document.getElementById('editarComentarioForm');
    form.action = form.action.replace('', id_comentario);

    var myModal = new bootstrap.Modal(document.getElementById('modalEditarComentario'));
    myModal.show();
}