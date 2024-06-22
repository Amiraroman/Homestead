function editarFacturacion(id_facturacion, numero_facturacion, monto, codigo_cuf, fecha_facturacion, id_pago) {
    document.getElementById('editarIdFacturacion').value = id_facturacion;
    document.getElementById('editarNumeroFacturacion').value = numero_facturacion;
    document.getElementById('editarMonto').value = monto;
    document.getElementById('editarCodigoCUF').value = codigo_cuf;
    document.getElementById('editarFechaFacturacion').value = fecha_facturacion;
    document.getElementById('editarIdPago').value = id_pago;

    var editarFacturacionForm = document.getElementById('editarFacturacionForm'); 

    editarFacturacionForm.action = '/facturacion/editar/' + id_facturacion;

    var myModal = new bootstrap.Modal(document.getElementById('modalEditarFacturacion'), {
        keyboard: false
    });
    myModal.show();
}

