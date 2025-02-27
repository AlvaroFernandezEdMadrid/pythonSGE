import mysql.connector
from mysql.connector import Error

class ConexionBBDD:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.connection = None

    def conectar(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                self.crearBbddTabla()
                return True
        except Error as e:
            print(f"Error de conexion: {e}")
            return False

    def crearBbddTabla(self):
        cursor = self.connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS bbddexamen")
        cursor.execute("USE bbddexamen")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS temperaturas (
                comunidad_autonoma VARCHAR(50),
                max INT,
                min INT
            )
        """)

        #Para no tener repetidos cada vez que ejecutamos
        cursor.execute("""
            DELETE FROM temperaturas;
        """)

        cursor.execute("""
            INSERT IGNORE INTO temperaturas (comunidad_autonoma, max, min)
            VALUES
            ('Comunidad de Madrid', 42, -4),
            ('Barcelona', 43, 1),
            ('Castilla la Mancha', 40, -6),
            ('Andalucia', 46, 2)
        """)
        self.connection.commit()
