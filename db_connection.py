import pyodbc

# Configuración de la conexión
server = 'DESKTOP-UNHKLES'  # Nombre del servidor
database = 'uptamca'  # Nombre de la base de datos
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

def get_connection():
    try:
        # Establecer la conexión
        connection = pyodbc.connect(connection_string)
        print("¡Conexión exitosa!")
        return connection
    except pyodbc.Error as ex:
        print("Error al conectar a la base de datos:", ex)
        return None