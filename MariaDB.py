import mysql.connector as mariadb


conexion = mariadb.connect(
    host='localhost',
    port=3307,
    user='root',
    password='123456',
    db='diccionario'   
    )

def crear_tablas():
    cursor = conexion.cursor()
    return cursor.execute("CREATE TABLE IF NOT EXISTS diccionario (id INT AUTO_INCREMENT PRIMARY KEY, palabra VARCHAR(255), significado VARCHAR(255))")

def principal():
    crear_tablas()
    menu="""
a) Agregar nueva palabra
b) Editar palabra existente
c) Eliminar palabra existente
d) Ver listado de palabras
e) Buscar significado de palabra
f) Salir
Elige: """
    eleccion = ""
    while eleccion != "f":
        eleccion = input(menu)
        if eleccion == "a":
            palabra = input("Ingresa la palabra: ")
            # Comprobar si no existe
            posible_significado = buscar_significado_palabra(palabra)
            if posible_significado:
                print(f"La palabra '{palabra}' ya existe")
            else:
                significado = input("Ingresa el significado: ")
                agregar_palabra(palabra, significado)
                print("Palabra agregada")
        if eleccion == "b":
            palabra = input("Ingresa la palabra que quieres editar: ")
            nuevo_significado = input("Ingresa el nuevo significado: ")
            editar_palabra(palabra, nuevo_significado)
            print("Palabra actualizada")
        if eleccion == "c":
            palabra = input("Ingresa la palabra a eliminar: ")
            eliminar_palabra(palabra)
        if eleccion == "d":
            palabras = obtener_palabras()
            print("=== Lista de palabras ===")
            for palabra in palabras:
                # Al leer desde la base de datos se devuelven los datos como arreglo, por
                # lo que hay que imprimir el primer elemento
                print(palabra[0])
        if eleccion == "e":
            palabra = input(
                "Ingresa la palabra de la cual quieres saber el significado: ")
            significado = buscar_significado_palabra(palabra)
            if significado:
                print(f"El significado de '{palabra}' es:\n{significado[0]}")
            else:
                print(f"Palabra '{palabra}' no encontrada")

def agregar_palabra(palabra, significado):
    cursor = conexion.cursor()
    sentencia = "INSERT INTO diccionario (palabra, significado) VALUES (%s, %s)"
    cursor.execute(sentencia, [palabra, significado])
    conexion.commit()

def editar_palabra(palabra, nuevo_significado):
    cursor = conexion.cursor()
    sentencia = "UPDATE diccionario SET significado = %s WHERE palabra = %s"
    cursor.execute(sentencia, [nuevo_significado, palabra])
    conexion.commit()

def eliminar_palabra(palabra):
    cursor = conexion.cursor()
    sentencia = "DELETE FROM diccionario WHERE palabra = %s"
    cursor.execute(sentencia, [palabra])
    conexion.commit()

def obtener_palabras():
    cursor = conexion.cursor()
    consulta = "SELECT palabra FROM diccionario"
    cursor.execute(consulta)
    return cursor.fetchall()

def buscar_significado_palabra(palabra):
    cursor = conexion.cursor()
    consulta = "SELECT significado FROM diccionario WHERE palabra = %s"
    cursor.execute(consulta, [palabra])
    return cursor.fetchone()

if __name__ == '__main__':
    principal()