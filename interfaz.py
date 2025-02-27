import tkinter as tk
from PIL import Image, ImageTk
from colores import Colores
from datetime import datetime
import threading
from conexDb import ConexionBBDD
from crearGrafica import crear_grafica
from generarPdf import generar_pdf


# Funcion para borrar contenido de un frame
def deleteInFrames(frame):
    for widget in frame.winfo_children():
        widget.destroy()

class Interfaz(tk.Tk):
    def __init__(self, title, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.title(title)
        
        # Instanciar Colores
        self.colores = Colores()

        # Variable para mantener la conex abierta
        self.conexion = None
        
        # Centrar ventana en la pantalla
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (self.width // 2)
        y = (pantalla_alto // 2) - (self.height // 2)
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.resizable(False, False)
        
        # Configurar grid weights
        self.grid_columnconfigure(1, weight=1, minsize=600)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(2, weight=0)
        
        # Header Frame
        self.header = tk.Frame(
            self,
            bg=self.colores.getAzulClaro(),
            height=120
        )
        self.header.grid(row=0, column=0, sticky="ew", columnspan=3)
        self.header.grid_propagate(False)

        # Label alumno
        self.label_nombre_alumno = tk.Label(
            self.header,
            text="Nombre del Alumno",
            bg=self.colores.getAzulClaro(),
            fg=self.colores.getNegro(),
            font=("Helvetica", 16, "bold"),
            padx=20
        )
        self.label_nombre_alumno.grid(row=0, column=0, sticky="w", pady=30)

        # Sidebar Frame
        self.sidebar = tk.Frame(
            self,
            bg=self.colores.getAzulOscuro(),
            width=250 
        )
        self.sidebar.grid(row=1, column=0, sticky="ns", rowspan=2)
        self.sidebar.grid_propagate(False)
        
        # Cargar imagen y ajustar tamanio
        self.logo_image = Image.open("logo.png")
        new_width = int(self.logo_image.width * 0.3)
        new_height = int(self.logo_image.height * 0.3)
        self.logo_image = self.logo_image.resize((new_width, new_height))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        
        # Label para imagen
        self.logo_label = tk.Label(self.sidebar, image=self.logo_photo, bg=self.colores.getAzulOscuro())
        self.logo_label.grid(row=0, column=0, pady=20)

        # Estilo de los botones
        button_style = {
            "bg": self.colores.getAzulClaro(),
            "fg": self.colores.getBlanco(),
            "font": ("Helvetica", 14), 
            "width": 20,                
            "height": 2                 
        }
        
        # Botones del sidebar
        self.btn_conexion_bbdd = tk.Button(self.sidebar, text="Conexion BBDD", **button_style, 
                                           command=lambda: threading.Thread(target=self.conectar_bbdd, daemon=True).start())
        self.btn_conexion_bbdd.grid(row=1, column=0, pady=10)
        
        self.btn_generar_grafica = tk.Button(self.sidebar, text="Generar Grafica", **button_style, 
                                             command=lambda: threading.Thread(target=self.generar_grafica, daemon=True).start())
        self.btn_generar_grafica.grid(row=2, column=0, pady=10)
        
        self.btn_generar_pdf = tk.Button(self.sidebar, text="Generar PDF", **button_style, 
                                         command=lambda: threading.Thread(target=self.generar_pdf, daemon=True).start())  
        self.btn_generar_pdf.grid(row=3, column=0, pady=10)
        
        # Content Frame
        self.content = tk.Frame(
            self,
            bg=self.colores.getPrueba()
        )
        self.content.grid(row=1, column=1, sticky="nsew")
        self.content.grid_propagate(False)
        
        # Footer Frame
        self.footer = tk.Frame(
            self,
            bg=self.colores.getAzulClaro(),
            height=120
        )
        self.footer.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.footer.grid_propagate(False)

        # Configuracion footer
        self.footer.grid_columnconfigure(0, weight=1) 
        self.footer.grid_columnconfigure(1, weight=1)
        self.footer.grid_columnconfigure(2, weight=0)
        
        # Btn acerca de
        self.btn_acerca_de = tk.Button(self.footer, text="Acerca de...", **button_style, command=self.mostrar_acerca_de)
        self.btn_acerca_de.grid(row=0, column=2, sticky="e", padx=20, pady=30)

    def conectar_bbdd(self):
        if self.conexion is None:
            self.conexion = ConexionBBDD(host="localhost", user="root", password="123456")
            if self.conexion.conectar():
                self.mostrar_mensaje("Conexion exitosa")
            else:
                self.mostrar_mensaje("Error de conexion")

    def generar_grafica(self):
        deleteInFrames(self.content)

        crear_grafica(self.conexion, self.content)

    def generar_pdf(self):
        if self.conexion:
            generar_pdf(self.conexion)
        else:
            self.mostrar_mensaje("Primero debes conectar con la base de datos.")

    def mostrar_mensaje(self, mensaje):
        deleteInFrames(self.content)
        label_mensaje = tk.Label(self.content, text=mensaje, font=("Helvetica", 16, "bold"), fg="green", bg=self.colores.azulClaro)
        label_mensaje.pack(pady=50)

    def mostrar_acerca_de(self):
        # Crear ventana hija
        ventana_hija = tk.Toplevel(self)
        ventana_hija.title("Acerca de...")
        
        # Centrar ventana hija
        pantalla_ancho = ventana_hija.winfo_screenwidth()
        pantalla_alto = ventana_hija.winfo_screenheight()
        
        ancho_ventana = 300
        alto_ventana = 200
        
        x = (pantalla_ancho // 2) - (ancho_ventana // 2)
        y = (pantalla_alto // 2) - (alto_ventana // 2)
        ventana_hija.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        acerca_de = tk.Frame(ventana_hija)
        acerca_de.grid(row=0, column=0, padx=10, pady=10)

        # Info
        nombre = "nombrealumno"
        ciclo = "DAM2"
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")

        # Labels con la info
        label_nombre = tk.Label(acerca_de, text=f"Nombre: {nombre}", font=("Helvetica", 12))
        label_nombre.grid(row=0, column=0, pady=5)
        
        label_ciclo = tk.Label(acerca_de, text=f"Ciclo: {ciclo}", font=("Helvetica", 12))
        label_ciclo.grid(row=1, column=0, pady=5)
        
        label_fecha = tk.Label(acerca_de, text=f"Fecha: {fecha_hoy}", font=("Helvetica", 12))
        label_fecha.grid(row=2, column=0, pady=5)

