from db_connection import get_connection
import pyodbc

# Obtener la conexión a la base de datos
connection = get_connection()

# Función para crear un nuevo alumno
def create_alumno(cedula, nombre, apellido):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO alumnos (cedula, nombre, apellido) VALUES (?, ?, ?)", (cedula, nombre, apellido))
        connection.commit()
        print("Alumno creado exitosamente.")
    except pyodbc.Error as ex:
        print("Error al crear alumno:", ex)
    finally:
        cursor.close()

# Función para leer todos los alumnos
def read_alumnos():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM alumnos")
        rows = cursor.fetchall()
        if not rows:
            print("No hay alumnos registrados.")
            return False
        for row in rows:
            print(f'ID: {row[0]}, Cédula: {row[1]}, Nombre: {row[2]}, Apellido: {row[3]}')

        print("\nMaterias Asignadas:")
        cursor.execute("""
            SELECT m.nombre
            FROM alumnos a
            JOIN alumnos_materias am ON a.id = am.alumno_id
            JOIN materias m ON am.materia_id = m.id
        """)
        materias = cursor.fetchall()
        if materias:
            for materia in materias:
                print(f"- {materia[0]}")
        else:
            print("Ninguna")
        return True
    except pyodbc.Error as ex:
        print("Error al leer alumnos:", ex)
        return False
    finally:
        cursor.close()

# Función para actualizar un alumno existente
def update_alumno(id, cedula, nombre, apellido):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM alumnos WHERE id = ?", (id,))
        if cursor.fetchone():
            cursor.execute("UPDATE alumnos SET cedula = ?, nombre = ?, apellido = ? WHERE id = ?", (cedula, nombre, apellido, id))
            connection.commit()
            print("Alumno actualizado exitosamente.")
        else:
            print("ID de alumno no encontrado.")
    except pyodbc.Error as ex:
        print("Error al actualizar alumno:", ex)
    finally:
        cursor.close()

# Función para eliminar un alumno
def delete_alumno(id):
    cursor = connection.cursor()
    try:
        # Check if alumno has assigned materias
        cursor.execute("SELECT COUNT(*) FROM alumnos_materias WHERE alumno_id = ?", (id,))
        count = cursor.fetchone()[0]
        if count > 0:
            print("No se puede eliminar el alumno. Tiene materias asignadas.")
            return
        
        cursor.execute("SELECT id FROM alumnos WHERE id = ?", (id,))
        if cursor.fetchone():
            cursor.execute("DELETE FROM alumnos WHERE id = ?", (id,))
            connection.commit()
            print("Alumno eliminado exitosamente.")
        else:
            print("ID de alumno no encontrado.")
    except pyodbc.Error as ex:
        print("Error al eliminar alumno:", ex)
    finally:
        cursor.close()

# Función para leer la información de todas las tablas con INNER JOIN
def read_all_info():
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT alumnos.id as ID_Alumno, alumnos.cedula AS Cedula_Alumno, alumnos.nombre AS Nombre_Alumno,
                   profesores.nombre AS Nombre_Prof,
                   materias.nombre AS Nombre_Materia
            FROM materias
            INNER JOIN alumnos_materias ON materias.id = alumnos_materias.materia_id
            INNER JOIN alumnos ON alumnos_materias.alumno_id = alumnos.id
            INNER JOIN profesores_materias ON materias.id = profesores_materias.materia_id
            INNER JOIN profesores ON profesores_materias.profesor_id = profesores.id
        """)
        rows = cursor.fetchall()
        if not rows:
            print("No hay información disponible.")
            return False
        for row in rows:
            print(f'Alumno ID: {row[0]}, Cédula Alumno: {row[1]}, Nombre Alumno: {row[2]}, Profesor: {row[3]}, Materia: {row[4]}')
        return True
    except pyodbc.Error as ex:
        print("Error al leer información:", ex)
        return False
    finally:
        cursor.close()

# Función para crear un nuevo profesor
def create_profesor(cedula, nombre, apellido):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO profesores (cedula, nombre, apellido) VALUES (?, ?, ?)", (cedula, nombre, apellido))
        connection.commit()
        print("Profesor creado exitosamente.")
    except pyodbc.Error as ex:
        print("Error al crear profesor:", ex)
    finally:
        cursor.close()

# Función para leer todos los profesores
def read_profesores():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM profesores")
        rows = cursor.fetchall()
        if not rows:
            print("No hay profesores registrados.")
            return False
        for row in rows:
            print(f'ID: {row[0]}, Cédula: {row[1]}, Nombre: {row[2]}, Apellido: {row[3]}')
        
        print("\nMaterias Asignadas:")
        cursor.execute("""
            SELECT m.nombre
            FROM profesores p
            JOIN profesores_materias pm ON p.id = pm.profesor_id
            JOIN materias m ON pm.materia_id = m.id
        """)
        materias = cursor.fetchall()
        if materias:
            for materia in materias:
                print(f"- {materia[0]}")
        else:
            print("Ninguna")
        return True
    except pyodbc.Error as ex:
        print("Error al leer profesores:", ex)
        return False
    finally:
        cursor.close()

# Función para actualizar un profesor existente
def update_profesor(id, cedula, nombre, apellido):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM profesores WHERE id = ?", (id,))
        if cursor.fetchone():
            cursor.execute("UPDATE profesores SET cedula = ?, nombre = ?, apellido = ? WHERE id = ?", (cedula, nombre, apellido, id))
            connection.commit()
            print("Profesor actualizado exitosamente.")
        else:
            print("ID de profesor no encontrado.")
    except pyodbc.Error as ex:
        print("Error al actualizar profesor:", ex)
    finally:
        cursor.close()

# Función para eliminar un profesor
def delete_profesor(id):
    cursor = connection.cursor()
    try:
        # Check if profesor has assigned materias
        cursor.execute("SELECT COUNT(*) FROM profesores_materias WHERE profesor_id = ?", (id,))
        count = cursor.fetchone()[0]
        if count > 0:
            print("No se puede eliminar el profesor. Tiene materias asignadas.")
            return

        cursor.execute("SELECT id FROM profesores WHERE id = ?", (id,))
        if cursor.fetchone():
            cursor.execute("DELETE FROM profesores WHERE id = ?", (id,))
            connection.commit()
            print("Profesor eliminado exitosamente.")
        else:
            print("ID de profesor no encontrado.")
    except pyodbc.Error as ex:
        print("Error al eliminar profesor:", ex)
    finally:
        cursor.close()

# Función para crear una nueva materia
def create_materia(nombre, descripcion, creditos, codigo):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO materias (nombre, descripcion, creditos, codigo) VALUES (?, ?, ?, ?)", (nombre, descripcion, creditos, codigo))
        connection.commit()
        print("Materia creada exitosamente.")
    except pyodbc.Error as ex:
        print("Error al crear materia:", ex)
    finally:
        cursor.close()

# Función para leer todas las materias
def read_materias():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM materias")
        rows = cursor.fetchall()
        if not rows:
            print("No hay materias registradas.")
            return False
        for row in rows:
            print(f'ID: {row[0]}, Nombre: {row[1]}, Descripción: {row[2]}, Créditos: {row[3]}, Código: {row[4]}')
        return True
    except pyodbc.Error as ex:
        print("Error al leer materias:", ex)
        return False
    finally:
        cursor.close()

# Función para actualizar una materia existente
def update_materia(id, nombre, descripcion, creditos, codigo):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM materias WHERE id = ?", (id,))
        if cursor.fetchone():
            cursor.execute("UPDATE materias SET nombre = ?, descripcion = ?, creditos = ?, codigo = ? WHERE id = ?", (nombre, descripcion, creditos, codigo, id))
            connection.commit()
            print("Materia actualizada exitosamente.")
        else:
            print("ID de materia no encontrado.")
    except pyodbc.Error as ex:
        print("Error al actualizar materia:", ex)
    finally:
        cursor.close()

# Función para eliminar una materia
def delete_materia(id):
    cursor = connection.cursor()
    try:
        # Check if materia is assigned to alumnos or profesores
        cursor.execute("SELECT COUNT(*) FROM alumnos_materias WHERE materia_id = ?", (id,))
        count_alumnos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM profesores_materias WHERE materia_id = ?", (id,))
        count_profesores = cursor.fetchone()[0]
        if count_alumnos > 0 or count_profesores > 0:
            print("No se puede eliminar la materia. Está asignada a alumnos o profesores.")
            return

        cursor.execute("SELECT id FROM materias WHERE id = ?", (id,))
        if cursor.fetchone():
            cursor.execute("DELETE FROM materias WHERE id = ?", (id,))
            connection.commit()
            print("Materia eliminada exitosamente.")
        else:
            print("ID de materia no encontrado.")
    except pyodbc.Error as ex:
        print("Error al eliminar materia:", ex)
    finally:
        cursor.close()

# Función para asignar un profesor a una materia
def assign_profesor_to_materia(profesor_id, materia_id):
    cursor = connection.cursor()
    try:
        # Check if profesor and materia exist
        cursor.execute("SELECT id FROM profesores WHERE id = ?", (profesor_id,))
        if not cursor.fetchone():
            print("ID de profesor no encontrado.")
            return
        cursor.execute("SELECT id FROM materias WHERE id = ?", (materia_id,))
        if not cursor.fetchone():
            print("ID de materia no encontrado.")
            return

        # Check if the assignment already exists
        cursor.execute("SELECT * FROM profesores_materias WHERE profesor_id = ? AND materia_id = ?", (profesor_id, materia_id))
        if cursor.fetchone():
            print("La asignación ya existe.")
            return

        cursor.execute("INSERT INTO profesores_materias (profesor_id, materia_id) VALUES (?, ?)", (profesor_id, materia_id))
        connection.commit()
        print("Profesor asignado a la materia exitosamente.")
    except pyodbc.Error as ex:
        print("Error al asignar profesor a materia:", ex)
    finally:
        cursor.close()

# Función para asignar un alumno a una materia
def assign_alumno_to_materia(alumno_id, materia_id):
    cursor = connection.cursor()
    try:
        # Check if alumno and materia exist
        cursor.execute("SELECT id FROM alumnos WHERE id = ?", (alumno_id,))
        if not cursor.fetchone():
            print("ID de alumno no encontrado.")
            return
        cursor.execute("SELECT id FROM materias WHERE id = ?", (materia_id,))
        if not cursor.fetchone():
            print("ID de materia no encontrado.")
            return
        
        # Check if the assignment already exists
        cursor.execute("SELECT * FROM alumnos_materias WHERE alumno_id = ? AND materia_id = ?", (alumno_id, materia_id))
        if cursor.fetchone():
            print("La asignación ya existe.")
            return

        cursor.execute("INSERT INTO alumnos_materias (alumno_id, materia_id) VALUES (?, ?)", (alumno_id, materia_id))
        connection.commit()
        print("Alumno asignado a la materia exitosamente.")
    except pyodbc.Error as ex:
        print("Error al asignar alumno a materia:", ex)
    finally:
        cursor.close()

def cargar_notas_alumno(alumno_id, materia_id, nota):
    """
    Función para cargar notas de un alumno en una materia.
    ***Nota:*** Esta función asume que tienes una tabla 'notas' con las columnas
    'alumno_id', 'materia_id' y 'nota'.  ***Ajusta la consulta SQL según tu esquema de base de datos.***
    """
    cursor = connection.cursor()
    try:
        # Verificar si existe la asignación alumno-materia
        cursor.execute("SELECT * FROM alumnos_materias WHERE alumno_id = ? AND materia_id = ?", (alumno_id, materia_id))
        if not cursor.fetchone():
            print("El alumno no está asignado a esta materia.")
            return

        # Verificar si ya existe una nota (opcional, depende de tu lógica)
        cursor.execute("SELECT * FROM notas WHERE alumno_id = ? AND materia_id = ?", (alumno_id, materia_id))
        if cursor.fetchone():
            print("Ya existe una nota para este alumno en esta materia. Considere actualizarla.")
            return

        cursor.execute("INSERT INTO notas (alumno_id, materia_id, nota) VALUES (?, ?, ?)", (alumno_id, materia_id, nota))
        connection.commit()
        print("Nota cargada exitosamente.")

    except pyodbc.Error as ex:
        print("Error al cargar la nota:", ex)
    finally:
        cursor.close()


# Función para cerrar la conexión
def close_connection():
    connection.close()