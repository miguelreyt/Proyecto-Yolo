from funciones_CRUD import (
    create_alumno, read_alumnos, update_alumno, delete_alumno,
    create_profesor, read_profesores, update_profesor, delete_profesor,
    create_materia, read_materias, update_materia, delete_materia,
    assign_profesor_to_materia, assign_alumno_to_materia, cargar_notas_alumno,
    close_connection
)

def menu():
    while True:
        print("\nMenú:")
        print("1.  Crear Alumno")
        print("2.  Leer Alumnos")
        print("3.  Actualizar Alumno")
        print("4.  Eliminar Alumno")
        print("5.  Crear Profesor")
        print("6.  Leer Profesores")
        print("7.  Actualizar Profesor")
        print("8.  Eliminar Profesor")
        print("9.  Crear Materia")
        print("10. Leer Materias")
        print("11. Actualizar Materia")
        print("12. Eliminar Materia")
        print("13. Asignar Profesor a Materia")
        print("14. Asignar Alumno a Materia")
        print("15. Cargar Notas de Alumno")
        print("16. Salir")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            cedula = input("Ingrese la cédula del alumno: ")
            nombre = input("Ingrese el nombre del alumno: ")
            apellido = input("Ingrese el apellido del alumno: ")
            create_alumno(cedula, nombre, apellido)
        elif choice == '2':
            read_alumnos()
        elif choice == '3':
            id = int(input("Ingrese el ID del alumno a actualizar: "))
            cedula = input("Ingrese la nueva cédula: ")
            nombre = input("Ingrese el nuevo nombre: ")
            apellido = input("Ingrese el nuevo apellido: ")
            update_alumno(id, cedula, nombre, apellido)
        elif choice == '4':
            id = int(input("Ingrese el ID del alumno a eliminar: "))
            delete_alumno(id)
        elif choice == '5':
            cedula = input("Ingrese la cédula del profesor: ")
            nombre = input("Ingrese el nombre del profesor: ")
            apellido = input("Ingrese el apellido del profesor: ")
            create_profesor(cedula, nombre, apellido)
        elif choice == '6':
            read_profesores()
        elif choice == '7':
            id = int(input("Ingrese el ID del profesor a actualizar: "))
            cedula = input("Ingrese la nueva cédula: ")
            nombre = input("Ingrese el nuevo nombre: ")
            apellido = input("Ingrese el nuevo apellido: ")
            update_profesor(id, cedula, nombre, apellido)
        elif choice == '8':
            id = int(input("Ingrese el ID del profesor a eliminar: "))
            delete_profesor(id)
        elif choice == '9':
            nombre = input("Ingrese el nombre de la materia: ")
            descripcion = input("Ingrese la descripción de la materia: ")
            creditos = int(input("Ingrese los créditos de la materia: "))
            codigo = input("Ingrese el código de la materia: ")
            create_materia(nombre, descripcion, creditos, codigo)
        elif choice == '10':
            read_materias()
        elif choice == '11':
            id = int(input("Ingrese el ID de la materia a actualizar: "))
            nombre = input("Ingrese el nuevo nombre: ")
            descripcion = input("Ingrese la nueva descripción: ")
            creditos = int(input("Ingrese los nuevos créditos: "))
            codigo = input("Ingrese el nuevo código: ")
            update_materia(id, nombre, descripcion, creditos, codigo)
        elif choice == '12':
            id = int(input("Ingrese el ID de la materia a eliminar: "))
            delete_materia(id)
        elif choice == '13':
            profesor_id = int(input("Ingrese el ID del profesor: "))
            materia_id = int(input("Ingrese el ID de la materia: "))
            assign_profesor_to_materia(profesor_id, materia_id)
        elif choice == '14':
            alumno_id = int(input("Ingrese el ID del alumno: "))
            materia_id = int(input("Ingrese el ID de la materia: "))
            assign_alumno_to_materia(alumno_id, materia_id)
        elif choice == '15':
            alumno_id = int(input("Ingrese el ID del alumno: "))
            materia_id = int(input("Ingrese el ID de la materia: "))
            nota = float(input("Ingrese la nota del alumno: "))
            cargar_notas_alumno(alumno_id, materia_id, nota)
        elif choice == '16':
            close_connection()
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()