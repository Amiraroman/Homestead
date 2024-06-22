
function editarPago(id_pago, fecha_pago, metodo_pago, monto_pago, estado_pago, id_cliente) {
    document.getElementById('editarIdPago').value = id_pago;
    document.getElementById('editarFechaPago').value = fecha_pago;
    document.getElementById('editarMetodoPago').value = metodo_pago;
    document.getElementById('editarMontoPago').value = monto_pago;
    document.getElementById('editarEstadoPago').value = estado_pago;
    document.getElementById('editarIdCliente').value = id_cliente;

    var editarPagoForm = document.getElementById('editarPagoForm');
    editarPagoForm.action = '/pago/editar/' + id_pago;
    
    var modalEditarPago = new bootstrap.Modal(document.getElementById('modalEditarPago'), {
        keyboard: false
    });
    modalEditarPago.show();
}
