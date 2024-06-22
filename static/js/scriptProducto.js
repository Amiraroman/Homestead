
function editarProducto(id_producto, nombre, descripcion, precio, stock, id_categoria, marca, dimensiones, peso) {
    document.getElementById('editarIdProducto').value = id_producto;
    document.getElementById('editarNombre').value = nombre;
    document.getElementById('editarDescripcion').value = descripcion;
    document.getElementById('editarPrecio').value = precio;
    document.getElementById('editarStock').value = stock;
    document.getElementById('editarCategoria').value = id_categoria;
    document.getElementById('editarMarca').value = marca;
    document.getElementById('editarDimensiones').value = dimensiones;
    document.getElementById('editarPeso').value = peso;


    var editarProductoForm = document.getElementById('editarProductoForm'); 
    editarProductoForm.action = '/producto/editar/' + id_producto; 

  
    var myModal = new bootstrap.Modal(document.getElementById('modalEditarProducto'), {
        keyboard: false
    });
    myModal.show();
}

