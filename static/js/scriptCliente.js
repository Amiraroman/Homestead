// Función para cargar los datos de la habitación seleccionada en la modal de edición
function editarCliente(id_cliente, nombre, apellido, correo_electronico, direccion, ciudad, pais, telefono) {
    document.getElementById('editarIdCliente').value = id_cliente;
    document.getElementById('editarNombre').value = nombre;
    document.getElementById('editarApellido').value = apellido;
    document.getElementById('editarCorreoElectronico').value = correo_electronico;
    document.getElementById('editarDireccion').value = direccion;
    document.getElementById('editarCiudad').value = ciudad;
    document.getElementById('editarPais').value = pais;
    document.getElementById('editarTelefono').value = telefono;

    var editarClienteForm = document.getElementById('editarClienteForm'); 
    editarClienteForm.action = '/cliente/editar/' + id_cliente; 

   
    var myModal = new bootstrap.Modal(document.getElementById('modalEditarCliente'), {
        keyboard: false
    });
    myModal.show();
}






 