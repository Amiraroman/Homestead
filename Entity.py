from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Text, Time, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import or_,and_
from sqlalchemy import exists
from sqlalchemy import text,desc
from sqlalchemy.exc import IntegrityError

Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    contraseña = Column(String(100), nullable=False)
    clientes = relationship("Cliente", back_populates="usuario")

    @staticmethod
    def agregar_usuario(session, nombre_usuario, contraseña):
        existing_user = session.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
        if existing_user:
            print(f"Error: El nombre de usuario '{nombre_usuario}' ya existe.")
            return
        try:
            nuevo_usuario = Usuario(nombre_usuario=nombre_usuario, contraseña=contraseña)
            session.add(nuevo_usuario)
            session.commit()
            print("Usuario agregado correctamente")
        except IntegrityError as e:
            session.rollback()
            print("Error al agregar el usuario:", e)





    @staticmethod
    def modificar_usuario(session, id_usuario, **kwargs):
        usuario = session.query(Usuario).filter_by(id_usuario=id_usuario).first()
        if usuario:
            for key, value in kwargs.items():
                setattr(usuario, key, value)
            try:
                session.commit()
                print("Usuario actualizado")
            except IntegrityError as e:
                session.rollback()
                print("Error al actualizar el usuario:", e)
        else:
            print("Usuario no encontrado")

    @staticmethod
    def eliminar_usuario(session, id_usuario):
        usuario = session.query(Usuario).filter_by(id_usuario=id_usuario).first()
        if usuario:
            session.delete(usuario)
            session.commit()
            print("Usuario eliminado correctamente")
        else:
            print("Usuario no encontrado")

    @staticmethod
    def buscar_por_nombre_usuario(session, nombre_usuario):
        return session.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()

class Cliente(Base):
    __tablename__ = 'clientes'
    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    correo_electronico = Column(String(100))
    direccion = Column(String(255))
    ciudad = Column(String(100))
    pais = Column(String(100))
    telefono = Column(String(20))
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'))  
    usuario = relationship("Usuario", back_populates="clientes")
    direcciones = relationship("Direccion", back_populates="cliente")
    ordenes = relationship("Orden", back_populates="cliente")
    comentarios = relationship("ComentarioProducto", back_populates="cliente")
    pagos = relationship("Pago", back_populates="cliente")


    @staticmethod
    def mostrar_todos_los_clientes(session):
        clientes = session.query(Cliente).all()
        for cliente in clientes:
            print("ID de Cliente:", cliente.id_cliente)
            print("Nombre:", cliente.nombre)
            print("Apellido:", cliente.apellido)
            print("Correo Electrónico:", cliente.correo_electronico)
            print("Dirección:", cliente.direccion)
            print("Ciudad:", cliente.ciudad)
            print("País:", cliente.pais)
            print("Teléfono:", cliente.telefono)
            print("------------------------------------------")

    @staticmethod
    def agregar_cliente(session, nombre, apellido, correo_electronico, direccion, ciudad, pais, telefono, id_usuario):
        try:
            nuevo_cliente = Cliente(nombre=nombre, apellido=apellido, correo_electronico=correo_electronico,
                                    direccion=direccion, ciudad=ciudad, pais=pais, telefono=telefono, id_usuario=id_usuario)
            session.add(nuevo_cliente)
            session.flush()
            print("ID del Cliente generado:", nuevo_cliente.id_cliente)
            session.commit()
            print("Cliente agregado correctamente")
        except IntegrityError as e:
            session.rollback()
            print("Error al agregar el cliente:", e)

    @staticmethod
    def modificar_cliente(session, id_cliente, **kwargs):
        cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
        if cliente:
            for key, value in kwargs.items():
                setattr(cliente, key, value)
            try:
                session.commit()
                print("Cliente actualizado")
            except IntegrityError as e:
                session.rollback()
                print("Error al actualizar el cliente:", e)
        else:
            print("Cliente no encontrado")

    @staticmethod
    def eliminar_cliente(session, id_cliente):
        cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
        if cliente:
            try:
                for direccion in cliente.direcciones:
                    direccion.id_cliente = None
                session.delete(cliente)
                session.commit()
                print("Cliente eliminado correctamente")
            except IntegrityError as e:
                session.rollback()
                print("Error al eliminar el cliente:", e)
        else:
            print("Cliente no encontrado")


    @staticmethod
    def buscar_por_correo_electronico(session, correo_electronico):
        return session.query(Cliente).filter(Cliente.correo_electronico == correo_electronico).first()

    @staticmethod
    def calcular_total_gastado(session, id_cliente):
        ordenes = session.query(Orden).filter(Orden.id_cliente == id_cliente).all()
        total_gastado = sum(orden.total for orden in ordenes)
        return total_gastado

class Categoria(Base):
    __tablename__ = 'categorias'
    id_categoria = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = 'productos'
    id_producto = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    descripcion = Column(Text)
    precio = Column(Numeric(10, 2))
    stock = Column(Integer)
    categoria_id = Column(Integer, ForeignKey('categorias.id_categoria'))
    imagen = Column(String(255))
    marca = Column(String(100))
    dimensiones = Column(String(50))
    peso = Column(Numeric(10, 2))
    categoria = relationship("Categoria", back_populates="productos")
    comentarios = relationship("ComentarioProducto", back_populates="producto")
    inventario = relationship("Inventario", back_populates="producto")
   # carritos_compras = relationship("ProductoCarrito", back_populates="producto")

    @staticmethod
    def buscar_por_nombre(session, nombre_producto):
        return session.query(Producto).filter(Producto.nombre == nombre_producto).first()
    @staticmethod
    def obtener_producto_mas_caro(session):
        producto_mas_caro = session.query(Producto).order_by(Producto.precio.desc()).first()
        return producto_mas_caro

    @staticmethod
    def obtener_productos_por_categoria(session):
        productos_por_categoria = session.query(Producto.categoria_id, Categoria.nombre, func.count(Producto.id_producto)).\
                                join(Categoria, Producto.categoria_id == Categoria.id_categoria).\
                                group_by(Producto.categoria_id, Categoria.nombre).all()
        return productos_por_categoria
    @staticmethod
    def obtener_stock_total(session):
        stock_total = session.query(func.sum(Producto.stock)).scalar()
        return stock_total

    @staticmethod
    def agregarProducto(session, nombre, descripcion, precio, stock, categoria_id, imagen=None, marca=None, dimensiones=None, peso=None):
        nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, stock=stock, categoria_id=categoria_id, imagen=imagen, marca=marca, dimensiones=dimensiones, peso=peso)
        session.add(nuevo_producto)
        session.commit()
        print("Producto agregado correctamente")

    @staticmethod
    def modificarProducto(session, id_producto, **kwargs):
        producto = session.query(Producto).filter_by(id_producto=id_producto).first()
        if producto:
            for key, value in kwargs.items():
                setattr(producto, key, value)
            session.commit()
            print("Producto actualizado")
        else:
            print("Producto no encontrado")

    @staticmethod
    def eliminarProducto(session, id_producto):
        producto = session.query(Producto).filter_by(id_producto=id_producto).first()
        if producto:
            session.delete(producto)
            session.commit()
            print("Producto eliminado correctamente")
        else:
            print("Producto no encontrado")



class Direccion(Base):
    __tablename__ = 'direcciones'
    id_direccion = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False)
    calle = Column(String(45), nullable=False)
    latitud = Column(Numeric(10, 5), nullable=False)
    longitud = Column(Numeric(10, 5), nullable=False)
    edificio = Column(String(45))
    piso = Column(String(45))
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))
    cliente = relationship("Cliente", back_populates="direcciones")

class Orden(Base):
    __tablename__ = 'ordenes'
    id_orden = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))
    fecha = Column(Date, default=datetime.now)
    estado = Column(String(50))
    cliente = relationship("Cliente", back_populates="ordenes")

    @staticmethod
    def agregar_orden(session, id_cliente, estado):
        nueva_orden = Orden(id_cliente=id_cliente, estado=estado)
        session.add(nueva_orden)
        session.commit()
        print("Orden agregada correctamente")

    @staticmethod
    def modificar_orden(session, id_orden, **kwargs):
        orden = session.query(Orden).filter_by(id_orden=id_orden).first()
        if orden:
            for key, value in kwargs.items():
                setattr(orden, key, value)
            session.commit()
            print("Orden actualizada")
        else:
            print("Orden no encontrada")

    @staticmethod
    def eliminar_orden(session, id_orden):
        orden = session.query(Orden).filter_by(id_orden=id_orden).first()
        if orden:
            session.delete(orden)
            session.commit()
            print("Orden eliminada correctamente")
        else:
            print("Orden no encontrada")

  

    @staticmethod
    def contar_ordenes_por_estado(session):
        conteo_ordenes_por_estado = session.query(Orden.estado, func.count(Orden.id_orden)).\
                                group_by(Orden.estado).all()
        return conteo_ordenes_por_estado
    @staticmethod
    def mostrar_todas_las_ordenes(session):
        ordenes = session.query(Orden).all()
        for orden in ordenes:
            print("ID de Orden:", orden.id_orden)
            print("ID de Cliente:", orden.id_cliente)
            print("Fecha:", orden.fecha)
            print("Estado:", orden.estado)
            print("Total:", Orden.calcular_total_orden(session, orden.id_orden))
            print("------------------------------------------")



class ComentarioProducto(Base):
    __tablename__ = 'comentarios_productos'
    id_comentario = Column(Integer, primary_key=True)
    id_producto = Column(Integer, ForeignKey('productos.id_producto'))
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))
    comentario = Column(Text)
    puntuacion = Column(Integer)
    fecha = Column(Date, default=datetime.now)
    cliente = relationship("Cliente", back_populates="comentarios")
    producto = relationship("Producto", back_populates="comentarios")

    @staticmethod
    def agregar_comentario(session, id_producto, id_cliente, comentario, puntuacion, fecha=None):
        nuevo_comentario = ComentarioProducto(id_producto=id_producto, id_cliente=id_cliente, comentario=comentario, puntuacion=puntuacion)
        if fecha:
            nuevo_comentario.fecha = fecha
        session.add(nuevo_comentario)
        session.commit()
        print("Comentario agregado correctamente")

    @staticmethod
    def modificar_comentario(session, id_comentario, **kwargs):
        comentario = session.query(ComentarioProducto).filter_by(id_comentario=id_comentario).first()
        if comentario:
            for key, value in kwargs.items():
                setattr(comentario, key, value)
            session.commit()
            print("Comentario modificado")
        else:
            print("Comentario no encontrado")

    @staticmethod
    def eliminar_comentario(session, id_comentario):
        comentario = session.query(ComentarioProducto).filter_by(id_comentario=id_comentario).first()
        if comentario:
            session.delete(comentario)
            session.commit()
            print("Comentario eliminado correctamente")
        else:
            print("Comentario no encontrado")

    @staticmethod
    def obtener_comentarios_ordenados_por_fecha(session):
        comentarios_ordenados = session.query(ComentarioProducto).order_by(ComentarioProducto.fecha).all()
        return comentarios_ordenados

    

class CarritoCompra(Base):
    __tablename__ = 'carritos_compras'
    id_carrito = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))
    fecha = Column(Date, default=datetime.now)
    hora = Column(Time, nullable=False)
    ##cliente = relationship("Cliente", back_populates="CarritoCompra")

class ProductoCarrito(Base):
    __tablename__ = 'productos_carrito'
    id_carrito = Column(Integer, ForeignKey('carritos_compras.id_carrito'), primary_key=True)
    id_producto = Column(Integer, ForeignKey('productos.id_producto'), primary_key=True)
    cantidad = Column(Integer)
    producto = relationship("Producto", back_populates="productos_carrito", cascade="all, delete")
    #carrito = relationship("CarritoCompra", back_populates="productos")
    ##producto = relationship("Producto", back_populates="carritos_compras")
    # Define the relationship back to Producto in Producto class
    Producto.productos_carrito = relationship("ProductoCarrito", back_populates="producto")


class Inventario(Base):
    __tablename__ = 'inventario'
    id_inventario = Column(Integer, primary_key=True)
    id_producto = Column(Integer, ForeignKey('productos.id_producto'))
    cantidad = Column(Integer)
    producto = relationship("Producto", back_populates="inventario")


class Pago(Base):
    __tablename__ = 'pagos'
    id_pago = Column(Integer, primary_key=True)
    fecha_pago = Column(Date, nullable=False)
    metodo_pago = Column(String(25), nullable=False)
    monto_pago = Column(Numeric(18, 2), nullable=False)
    estado_pago = Column(String(10), nullable=False)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))
    cliente = relationship("Cliente", back_populates="pagos")


class Facturacion(Base):
    __tablename__ = 'facturacion'
    id_facturacion = Column(Integer, primary_key=True)
    numero_facturacion = Column(BigInteger, nullable=False)
    monto = Column(Numeric(18, 2), nullable=False)
    codigo_cuf = Column(String(100), nullable=False)
    fecha_facturacion = Column(Date, nullable=False)
    id_pago = Column(Integer, ForeignKey('pagos.id_pago'))
    pago = relationship("Pago")

    @staticmethod
    def agregar_facturacion(session, numero_facturacion, monto, codigo_cuf, fecha_facturacion, id_pago):
        nueva_facturacion = Facturacion(numero_facturacion=numero_facturacion, monto=monto, codigo_cuf=codigo_cuf, fecha_facturacion=fecha_facturacion, id_pago=id_pago)
        session.add(nueva_facturacion)
        session.commit()
        print("Facturación agregada correctamente")

    @staticmethod
    def modificar_facturacion(session, id_facturacion, **kwargs):
        facturacion = session.query(Facturacion).filter_by(id_facturacion=id_facturacion).first()
        if facturacion:
            for key, value in kwargs.items():
                setattr(facturacion, key, value)
            session.commit()
            print("Facturación modificada")
        else:
            print("Facturación no encontrada")

    @staticmethod
    def eliminar_facturacion(session, id_facturacion):
        facturacion = session.query(Facturacion).filter_by(id_facturacion=id_facturacion).first()
        if facturacion:
            session.delete(facturacion)
            session.commit()
            print("Facturación eliminada correctamente")
        else:
            print("Facturación no encontrada")


class TipoPago(Base):
    __tablename__ = 'tipo_pago'
    id_tipo_pago = Column(Integer, primary_key=True)
    token_seguridad = Column(String(45), unique=True)
    codigo_comprobante = Column(String(45), unique=True)
    id_pago = Column(Integer, ForeignKey('pagos.id_pago'))
    pago = relationship("Pago")

class Tarjeta(Base):
    __tablename__ = 'tarjetas'
    id_tarjeta = Column(Integer, primary_key=True)
    numero_tarjeta = Column(String(45))
    id_tipo_pago = Column(Integer, ForeignKey('tipo_pago.id_tipo_pago'))
    tipo_pago = relationship("TipoPago")


# FUNCIONES
#1
def obtener_productos_mas_vendidos(session):
    subquery = session.query(
        Producto.id_producto,
        Producto.nombre,
        func.sum(ProductoCarrito.cantidad).label('cantidad_vendida')
    ).join(
        ProductoCarrito, Producto.id_producto == ProductoCarrito.id_producto
    ).group_by(
        Producto.id_producto,
        Producto.nombre
    ).subquery()

    productos_mas_vendidos = session.query(
        subquery.c.nombre,
        subquery.c.cantidad_vendida
    ).order_by(
        subquery.c.cantidad_vendida.desc()
    ).all()

    return productos_mas_vendidos


#2
def obtener_clientes_mas_valiosos(session):
    
    resultados = session.query(Cliente.id_cliente, Cliente.nombre, func.sum(Facturacion.monto).label('monto_total')).\
        join(Pago, Cliente.id_cliente == Pago.id_cliente).\
        join(Facturacion, Pago.id_pago == Facturacion.id_pago).\
        group_by(Cliente.id_cliente, Cliente.nombre).\
        order_by(func.sum(Facturacion.monto).desc()).all()
    
    # Procesar los resultados
    for id_cliente, nombre_cliente, monto_total in resultados:
        print(f"ID del Cliente: {id_cliente}, Nombre del Cliente: {nombre_cliente}, Monto Total Gastado: {monto_total}")
#3
def obtener_ordenes_por_cliente(session, id_cliente_param):
    result = session.query(
        Cliente.nombre,
        Orden.id_orden,
        Orden.estado,
        func.count(Orden.id_orden) 
    ).filter(
        Cliente.id_cliente == id_cliente_param,
        Orden.id_cliente == Cliente.id_cliente
    ).group_by(
        Cliente.nombre,
        Orden.id_orden,
        Orden.estado
    ).all()
    
    return result

#4
def obtener_categoria_producto_mas_popular(session):
    result = session.query(
        Categoria.nombre
    ).join(
        Producto, Producto.categoria_id == Categoria.id_categoria
    ).group_by(
        Categoria.nombre
    ).order_by(
        func.count().desc()
    ).limit(1).scalar()
    
    return result
#5
def obtener_metodo_pago_mas_utilizado(session):
    result = session.query(
        Pago.metodo_pago,
        func.count().label('cantidad_usos')
    ).group_by(
        Pago.metodo_pago
    ).order_by(
        func.count().desc()
    ).limit(1).scalar()
    
    return result
#6
def obtener_valor_promedio_pedido(session):
    result = session.query(
        func.avg(Pago.monto_pago).label('valor_promedio')
    ).scalar()
    
    return result
#7
def autenticar_usuario(session, nombre_usuario_param, contrasena_param):
    usuario_autenticado = session.query(Usuario).\
        filter(
            Usuario.nombre_usuario == nombre_usuario_param,
            Usuario.contraseña == contrasena_param
        ).first()

    return usuario_autenticado is not None


#8
def obtener_productos_categoria(session, id_categoria_param):
    productos_categoria = session.query(Producto).\
        filter(Producto.categoria_id == id_categoria_param).all()

    return productos_categoria

#9


def calcular_total_carrito(session, id_carrito_param):
    detalles_carrito_temp = session.query(
        ProductoCarrito.id_producto,
        ProductoCarrito.cantidad,
        Producto.precio
    ).join(Producto, ProductoCarrito.id_producto == Producto.id_producto).filter(
        ProductoCarrito.id_carrito == id_carrito_param
    ).subquery()

    total = session.query(func.sum(detalles_carrito_temp.c.cantidad * detalles_carrito_temp.c.precio)).scalar()

    return total


#10
def obtener_comentarios_producto(session, id_producto_param):
    return session.query(ComentarioProducto).filter_by(id_producto=id_producto_param).all()

#11.1
def obtener_stock_producto(session, id_producto_param):
    nombre_producto, stock_producto = session.query(Producto.nombre, Producto.stock).\
        filter(Producto.id_producto == id_producto_param).\
        first()
    return nombre_producto, stock_producto
#11.2
def obtener_stock_todos_productos(session):
    productos = session.query(Producto.nombre, Producto.stock).all()
    return productos
#12
def obtener_cliente_con_mas_productos(session):
    query_result = session.query(
        Cliente.id_cliente,
        Cliente.nombre,
        func.count(ProductoCarrito.id_producto)
    ).select_from(Cliente).join(CarritoCompra).join(ProductoCarrito).group_by(
        Cliente.id_cliente,
        Cliente.nombre
    ).order_by(func.count(ProductoCarrito.id_producto).desc()).first()

    return query_result

#13
def obtener_estado_pago(session, id_pago_param):
    estado_pago_result = session.query(Pago.estado_pago).filter(Pago.id_pago == id_pago_param).scalar()
    return estado_pago_result
#14 ojito
def obtener_detalles_factura(session, id_cliente_param):
    detalles_factura = session.query(
        Facturacion.numero_facturacion,
        Facturacion.monto,
        Facturacion.codigo_cuf,
        Facturacion.fecha_facturacion,
        Facturacion.id_pago
    ).join(
        Pago
    ).filter(
        Pago.id_cliente == id_cliente_param
    ).all()

    return detalles_factura
#15
def obtener_metodos_pago_cliente(session, id_cliente_param):
    metodos_pago = session.query(
        Pago.metodo_pago
    ).filter(
        Pago.id_cliente == id_cliente_param
    ).distinct().all()

    metodos_pago_texto = [metodo.metodo_pago for metodo in metodos_pago]
    return metodos_pago_texto
#16
def obtener_clientes_con_pagos_pendientes(session):
    clientes_pagos_pendientes = session.query(
        Pago.id_cliente,
        Cliente.nombre,
        func.count('*').label('cantidad_pagos_pendientes')
    ).join(
        Cliente, Pago.id_cliente == Cliente.id_cliente
    ).filter(
        Pago.estado_pago == 'Pendiente'
    ).group_by(
        Pago.id_cliente, Cliente.nombre
    ).all()

    return clientes_pagos_pendientes