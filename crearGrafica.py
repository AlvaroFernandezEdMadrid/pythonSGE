import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from conexDb import ConexionBBDD

def crear_grafica(conexion, content_frame):
    # Conectar y obtener datos
    if conexion is not None and conexion.connection is not None:
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT comunidad_autonoma, max, min FROM temperaturas")
        resultados = cursor.fetchall()
        
        comunidades = []
        temperaturas_max = []
        temperaturas_min = []

        print(resultados)
        # Extraer datos
        for fila in resultados:
            
            comunidades.append(fila[0])  # Comunidad
            temperaturas_max.append(fila[1])  # Temp max
            temperaturas_min.append(fila[2])  # Temp min
       

        # Crear la figura y el eje
        fig, ax = plt.subplots()

        # Graficar lineas para temp max y min
        ax.plot(comunidades, temperaturas_max, label='Temperatura Maxima', color='red', marker='o')
        ax.plot(comunidades, temperaturas_min, label='Temperatura Minima', color='blue', marker='o')

        # Titulos y etiquetas
        ax.set_title('Temperaturas Anuales')
        ax.set_xlabel('Comunidades Autonomas')
        ax.set_ylabel('Temperatura (°C)')

        # Mostrar la leyenda
        ax.legend()

        # Guardar grafica como png
        fig.savefig("grafica_temperaturas.png")

        # Crear canvas
        canvas = FigureCanvasTkAgg(fig, master=content_frame)  # Integrar la fig en frame
        canvas.draw()

        # Colocar canvas en frame
        canvas.get_tk_widget().pack(fill='both', expand=True)  # Ajustar tamanio

    else:
        print("Error: No hay conexion a la bbdd.")
