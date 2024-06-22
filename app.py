from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from Entity import Base, Cliente,Producto,Categoria,Orden,Pago,ComentarioProducto,Facturacion

app = Flask(__name__)
app.secret_key = '123456'


engine = create_engine('postgresql://postgres:00000000@localhost/Homenestss')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bano')
def bano():
    return render_template('indices/bano.html')

#1.Ruta para  Cliente
@app.route('/cliente')
def listar_cliente():
    session = DBSession()
    clientes = session.query(Cliente).all()
    session.close()
    return render_template('cliente.html', clientes=clientes)

@app.route('/cliente/agregar', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        session = DBSession()
        try:
            nuevo_cliente = Cliente(
                nombre=request.form['nombre'],
                apellido=request.form['apellido'],
                correo_electronico=request.form['correo_electronico'],
                direccion=request.form['direccion'],
                ciudad=request.form['ciudad'],
                pais=request.form['pais'],
                telefono=request.form['telefono']
            )
            session.add(nuevo_cliente)
            session.commit()
            flash('Cliente agregado exitosamente!', 'success')
        except IntegrityError:
            session.rollback()
            flash('Error al agregar el cliente. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_cliente'))
    else:
        return render_template('agregar_cliente.html')

@app.route('/cliente/editar/<int:id_cliente>', methods=['GET', 'POST'])
def editar_cliente(id_cliente):
    session = DBSession()
    cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
    if request.method == 'POST':
        try:
            cliente.nombre = request.form['nombre']
            cliente.apellido = request.form['apellido']
            cliente.correo_electronico = request.form['correo_electronico']
            cliente.direccion = request.form['direccion']
            cliente.ciudad = request.form['ciudad']
            cliente.pais = request.form['pais']
            cliente.telefono = request.form['telefono']
            session.commit()
            flash('Cliente editado exitosamente!', 'success')
        except IntegrityError:
            session.rollback()
            flash('Error al editar el cliente. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_cliente'))
    else:
        session.close()
        return render_template('editar_cliente.html', cliente=cliente)
    

@app.route('/cliente/eliminar/<int:id_cliente>', methods=['GET', 'POST'])
def eliminar_cliente(id_cliente):
    session = DBSession()
    try:
        cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
        if cliente:
            session.delete(cliente)
            session.commit()
            flash('Cliente eliminado exitosamente!', 'success')
        else:
            flash('Cliente no encontrado.', 'danger')
    except IntegrityError:
        session.rollback()
        flash('Error al eliminar el cliente.', 'danger')
    finally:
        session.close()
    return redirect(url_for('listar_cliente'))










#2.Ruta para  Producto

@app.route('/producto')
def listar_producto():
    session = DBSession()
    try:
        productos = session.query(Producto).all()
        categorias = session.query(Categoria).all()
        return render_template('producto.html', productos=productos, categorias=categorias)
    finally:
        session.close()


@app.route('/producto/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        session = DBSession()
        try:
            nuevo_producto = Producto(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                precio=request.form['precio'],
                stock=request.form['stock'],
                categoria_id=request.form['id_categoria'], 
                marca=request.form['marca'],
                dimensiones=request.form['dimensiones'],
                peso=request.form.get('peso')
            )
            session.add(nuevo_producto)
            session.commit()
            flash('Producto agregado exitosamente!', 'success')
        except IntegrityError:
            session.rollback()
            flash('Error al agregar el producto. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_producto'))
    else:
        return render_template('agregar_producto.html')
    

@app.route('/producto/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    session = DBSession()
    producto = session.query(Producto).get(id_producto)

    if not producto:
        flash('Producto no encontrado.', 'danger')
        session.close()
        return redirect(url_for('listar_producto'))

    if request.method == 'POST':
        try:
            producto.nombre = request.form['nombre']
            producto.descripcion = request.form['descripcion']
            producto.precio = request.form['precio']
            producto.stock = request.form['stock']
            producto.categoria_id = request.form['id_categoria'] 
            producto.marca = request.form['marca']
            producto.dimensiones = request.form['dimensiones']
            producto.peso = request.form.get('peso')
            session.commit()
            flash('Producto editado exitosamente!', 'success')
        except IntegrityError:
            session.rollback()
            flash('Error al editar el producto. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_producto'))
    else:
        session.close()
        return render_template('editar_producto.html', producto=producto)


@app.route('/producto/eliminar/<int:id_producto>', methods=['GET', 'POST'])
def eliminar_producto(id_producto):
    session = DBSession()
    try:
        producto = session.query(Producto).filter_by(id_producto=id_producto).first()
        if producto:
            session.delete(producto)
            session.commit()
            flash('Producto eliminado exitosamente!', 'success')
        else:
            flash('Producto no encontrado.', 'danger')
    except IntegrityError:
        session.rollback()
        flash('Error al eliminar el producto.', 'danger')
    finally:
        session.close()
    return redirect(url_for('listar_producto'))







#3.Ruta para Orden

@app.route('/orden')
def listar_orden():
    session = DBSession()
    try:
        ordenes = session.query(Orden).all()
        clientes = session.query(Cliente).all()
        return render_template('orden.html', ordenes=ordenes, clientes=clientes)
    finally:
        session.close()

@app.route('/orden/agregar', methods=['GET', 'POST'])
def agregar_orden():
    if request.method == 'POST':
        session = DBSession()
        try:
            nueva_orden = Orden(
                fecha=request.form['fecha'],
                estado=request.form['estado'],
                id_cliente=request.form.get('id_cliente')
            )
            session.add(nueva_orden)
            session.commit()
            
        except IntegrityError:
            session.rollback()
            flash('Error al agregar la orden. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_orden'))
    else:
        return render_template('agregar_orden.html')
    
    

@app.route('/orden/editar/<int:id_orden>', methods=['GET', 'POST'])
def editar_orden(id_orden):
    session = DBSession()
    orden = session.query(Orden).filter_by(id_orden=id_orden).first()
    
    if request.method == 'POST':
        try:
            orden.fecha = request.form['fecha']
            orden.estado = request.form['estado']
            orden.id_cliente = request.form['editarIdCliente']
            session.commit()
        except IntegrityError:
            session.rollback()
            flash('Error al editar la orden. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_orden'))
    else:
        session.close()
        return render_template('editar_orden.html', orden=orden)



@app.route('/orden/eliminar/<int:id_orden>', methods=['GET', 'POST'])
def eliminar_orden(id_orden):
    session = DBSession()
    try:
        orden = session.query(Orden).filter_by(id_orden=id_orden).first()
        if orden:
            session.delete(orden)
            session.commit()
            
        else:
            flash('orden no encontrada.', 'danger')
    except IntegrityError:
        session.rollback()
        flash('Error al eliminar la orden.', 'danger')
    finally:
        session.close()
    
    return redirect(url_for('listar_orden'))




#4.Ruta para Pago


@app.route('/pago')
def listar_pago():
    session = DBSession()
    try:
        pagos = session.query(Pago).all()
        clientes = session.query(Cliente).all()  
        return render_template('pago.html', pagos=pagos, clientes=clientes)
    finally:
        session.close()

@app.route('/pago/agregar', methods=['GET', 'POST'])
def agregar_pago():
    if request.method == 'POST':
        session = DBSession()
        try:
            nuevo_pago = Pago(
                fecha_pago=request.form['fecha_pago'],
                metodo_pago=request.form['metodo_pago'],
                monto_pago=request.form['monto_pago'],
                estado_pago=request.form['estado_pago'],
                id_cliente=request.form.get('id_cliente')
            )
            session.add(nuevo_pago)
            session.commit()
        except IntegrityError:
            session.rollback()
            flash('Error al agregar el pago. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_pago'))
    else:
        return render_template('agregar_pago.html')

@app.route('/pago/editar/<int:id_pago>', methods=['GET', 'POST'])
def editar_pago(id_pago):
    session = DBSession()
    pago = session.query(Pago).filter_by(id_pago=id_pago).first()
    
    if request.method == 'POST':
        try:
            pago.fecha_pago = request.form['fecha_pago']
            pago.metodo_pago = request.form['metodo_pago']
            pago.monto_pago = request.form['monto_pago']
            pago.estado_pago = request.form['estado_pago']
            pago.id_cliente = request.form['editarIdClientePago']  
            session.commit()
        except IntegrityError:
            session.rollback()
            flash('Error al editar el pago. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_pago'))
    else:
        session.close()
        return render_template('editar_pago.html', pago=pago)


@app.route('/pago/eliminar/<int:id_pago>', methods=['GET', 'POST'])
def eliminar_pago(id_pago):
    session = DBSession()
    try:
        pago = session.query(Pago).filter_by(id_pago=id_pago).first()
        if pago:
            session.delete(pago)
            session.commit()
        else:
            flash('Pago no encontrado.', 'danger')
    except IntegrityError:
        session.rollback()
        flash('Error al eliminar el pago.', 'danger')
    finally:
        session.close()
    
    return redirect(url_for('listar_pago'))





#5.Ruta para Comentario Producto

@app.route('/comentario_producto')
def listar_comentarios():
    session = DBSession()
    try:
        comentarios = session.query(ComentarioProducto).all()
        clientes = session.query(Cliente).all()
        productos = session.query(Producto).all()

        return render_template('comentario_producto.html', comentarios=comentarios, clientes=clientes, productos=productos)
    finally:
        session.close()


@app.route('/comentario_producto/agregar', methods=['GET', 'POST'])
def agregar_comentario_producto():
    if request.method == 'POST':
        session = DBSession()
        try:
            nuevo_comentario = ComentarioProducto(
                comentario=request.form['comentario'],
                puntuacion=int(request.form['puntuacion']),
                id_cliente=int(request.form['id_cliente']),
                id_producto=int(request.form['id_producto']),
                fecha=request.form['fecha']
            )
            session.add(nuevo_comentario)
            session.commit()
            flash('Comentario agregado correctamente.', 'success')
        except Exception as e:
            session.rollback()
            flash(f'Error al agregar el comentario: {str(e)}', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_comentarios'))
    else:
        session = DBSession()
        try:
            clientes = session.query(Cliente).all()
            productos = session.query(Producto).all()
            return render_template('agregar_comentario.html', clientes=clientes, productos=productos)
        except Exception as e:
            flash(f'Error al cargar los datos del formulario: {str(e)}', 'danger')
            return redirect(url_for('listar_comentarios'))
        finally:
            session.close()




@app.route('/comentario_producto/editar/<int:id_comentario>', methods=['GET', 'POST'])
def editar_comentario(id_comentario):
    session = DBSession()
    comentario = session.query(ComentarioProducto).filter_by(id_comentario=id_comentario).first()
    
    if not comentario:
        flash('Comentario no encontrado.', 'danger')
        session.close()
        return redirect(url_for('listar_comentarios'))
    
    if request.method == 'POST':
        try:
            comentario.comentario = request.form['comentario']
            comentario.puntuacion = int(request.form['puntuacion'])
            comentario.fecha = request.form['fecha']
            comentario.id_cliente = int(request.form['id_cliente'])
            comentario.id_producto = int(request.form['id_producto'])
            
            session.commit()
            flash('Comentario actualizado correctamente.', 'success')
        except Exception as e:
            session.rollback()
            flash(f'Error al actualizar el comentario: {str(e)}', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_comentarios'))
    else:
        try:
            clientes = session.query(Cliente).all()
            productos = session.query(Producto).all()
            return render_template('editar_comentario.html', comentario=comentario, clientes=clientes, productos=productos)
        except Exception as e:
            flash(f'Error al cargar los datos del formulario: {str(e)}', 'danger')
            return redirect(url_for('listar_comentarios'))
        finally:
            session.close()


@app.route('/comentario_producto/eliminar/<int:id_comentario>', methods=['GET', 'POST'])
def eliminar_comentario(id_comentario):
    session = DBSession()
    try:
        comentario = session.query(ComentarioProducto).filter_by(id_comentario=id_comentario).first()
        if not comentario:
            flash('Comentario no encontrado.', 'danger')
        else:
            session.delete(comentario)
            session.commit()
            flash('Comentario eliminado correctamente.', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error al eliminar el comentario: {str(e)}', 'danger')
    finally:
        session.close()
    
    return redirect(url_for('listar_comentarios'))





#6.Ruta para Facturacion

@app.route('/facturacion')
def listar_facturacion():
    session = DBSession()
    facturaciones = session.query(Facturacion).all()
    session.close()
    return render_template('facturacion.html', facturaciones=facturaciones)



@app.route('/facturacion/agregar', methods=['GET', 'POST'])
def agregar_facturacion():
    if request.method == 'POST':
        session = DBSession()
        try:
            nueva_facturacion = Facturacion(
                numero_facturacion=request.form['numero_facturacion'],
                monto=request.form['monto'],
                codigo_cuf=request.form['codigo_cuf'],
                fecha_facturacion=request.form['fecha_facturacion'],
                id_pago=request.form.get('id_pago')
            )
            session.add(nueva_facturacion)
            session.commit()
            flash('Facturación agregada exitosamente!', 'success')
        except IntegrityError:
            session.rollback()
            flash('Error al agregar la facturación. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_facturacion'))
    else:
        return render_template('agregar_facturacion.html')
    



@app.route('/facturacion/editar/<int:id_facturacion>', methods=['GET', 'POST'])
def editar_facturacion(id_facturacion):
    session = DBSession()
    facturacion = session.query(Facturacion).filter_by(id_facturacion=id_facturacion).first()
    if request.method == 'POST':
        try:
            facturacion.numero_facturacion = request.form['numero_facturacion']
            facturacion.monto = request.form['monto']
            facturacion.codigo_cuf = request.form['codigo_cuf']
            facturacion.fecha_facturacion = request.form['fecha_facturacion']
            facturacion.id_pago = request.form['id_pago']
            session.commit()
            flash('facturacion editado exitosamente!', 'success')
        except IntegrityError:
            session.rollback()
            flash('Error al editar  facturacion. Verifique los datos.', 'danger')
        finally:
            session.close()
        return redirect(url_for('listar_facturacion'))
    else:
        session.close()
        return render_template('editar_facturacion.html', facturacion=facturacion)
    


@app.route('/facturacion/eliminar/<int:id_facturacion>', methods=['GET', 'POST'])
def eliminar_facturacion(id_facturacion):
    session = DBSession()
    try:
        facturacion = session.query(Facturacion).filter_by(id_facturacion=id_facturacion).first()
        if facturacion:
            session.delete(facturacion)
            session.commit()
            flash('Facturación eliminada exitosamente!', 'success')
        else:
            flash('Facturación no encontrada.', 'danger')
    except IntegrityError as e:
        session.rollback()
        flash(f'Error al eliminar la facturación. Error: {str(e)}', 'danger')
    finally:
        session.close()
    
    return redirect(url_for('listar_facturacion'))



if __name__ == '__main__':
    app.run(debug=True)
