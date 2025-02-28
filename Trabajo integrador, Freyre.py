import sqlite3

# Función para conectar a la base de datos
def conectar_db():
    return sqlite3.connect("inventario.db")

# Función para crear la tabla 'productos' si no existe
def crear_tabla():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    """)
    conexion.commit()
    conexion.close()

# Alta de productos nuevos
def alta_producto():
    conexion = conectar_db()
    cursor = conexion.cursor()

    nombre = input("Nombre del producto: ").strip().lower()  

    # Verifica si el producto ya existe
    cursor.execute("SELECT * FROM productos WHERE LOWER(nombre) = ?", (nombre,))
    producto = cursor.fetchone()

    if producto:
        print(f"\nError: El producto '{nombre}' ya existe en el inventario.")
        conexion.close()
        return  # Regresar al menú principal sin hacer nada

    descripcion = input("Descripción: ")
    try:
        cantidad = int(input("Cantidad en stock: "))
        precio = float(input("Precio: "))
        categoria = input("Categoría: ")

        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, descripcion, cantidad, precio, categoria))

        conexion.commit()
        print(f"\nProducto '{nombre}' añadido al inventario.")

    except ValueError:
        print("\nError: Ingresa valores numéricos válidos para cantidad y precio.")

    conexion.close()

# Consulta de productos
def consulta_productos():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    if productos:
        print("\n**** Productos en Inventario ****\n")
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[3]}, Precio: ${producto[4]}, Categoría: {producto[5]}")
    else:
        print("\nNo hay productos en el inventario.")

    conexion.close()

# Modificar cantidad de un producto
def modificar_cantidad():
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        id_producto = int(input("\nID del producto a modificar: "))
        nueva_cantidad = int(input("Nueva cantidad: "))

        cursor.execute("""
            UPDATE productos
            SET cantidad = ?
            WHERE id = ?
        """, (nueva_cantidad, id_producto))

        conexion.commit()

        if cursor.rowcount > 0:
            print("\nCantidad actualizada correctamente.")
        else:
            print("\nProducto no encontrado.")

        conexion.close()

    except ValueError:
        print("\nError: Ingresa valores numéricos para el ID y cantidad.")

# Eliminar un producto
def eliminar_producto():
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        id_producto = int(input("\nID del producto a eliminar: "))
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))

        conexion.commit()

        if cursor.rowcount > 0:
            print("\nProducto eliminado correctamente.")
        else:
            print("\nProducto no encontrado.")

        conexion.close()

    except ValueError:
        print("\nError: Ingresa un valor numérico para el ID.")

# Lista de productos con bajo stock
def reporte_bajo_stock():
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        limite = int(input("\nIngrese el límite para considerar bajo stock: "))
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
        productos = cursor.fetchall()

        if productos:
            print("\n**** Productos con Bajo Stock ****\n")
            for producto in productos:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[3]}, Precio: ${producto[4]}, Categoría: {producto[5]}")
        else:
            print("\nNo hay productos con bajo stock.")

        conexion.close()

    except ValueError:
        print("\nError: Ingresa valores numéricos para el límite.")

# Menú principal
def menu():
    crear_tabla()  # Asegurarse de crear la tabla antes de ejecutar cualquier opción

    while True:
        print("\n**** Menú de Gestión de Productos ****")
        print("1. Alta de productos nuevos")
        print("2. Consulta de datos de productos")
        print("3. Modificar la cantidad en stock de un producto")
        print("4. Dar de baja productos")
        print("5. Reporte de productos con bajo stock")
        print("6. Salir")

        opcion = input("\nSelecciona una opción (1-6): ")

        if opcion == "1":
            alta_producto()
        elif opcion == "2":
            consulta_productos()
        elif opcion == "3":
            modificar_cantidad()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            reporte_bajo_stock()
        elif opcion == "6":
            print("\n¡Hasta luego! Vuelve pronto.")
            break
        else:
            print("\nOpción no válida. Intenta de nuevo.")


menu()
