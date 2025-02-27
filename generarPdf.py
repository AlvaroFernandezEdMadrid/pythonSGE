import base64
import pdfkit
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def generar_pdf(conexion):
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    # Obtener datos de la bbdd
    cursor = conexion.connection.cursor()
    cursor.execute("SELECT * FROM temperaturas")
    registros = cursor.fetchall()

    # Cargar plantilla
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('plantilla_pdf.html')

    # Convertir imagen a base64, sino peta
    with open('grafica_temperaturas.png', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Crear URL base64
    ruta_imagen_base64 = f"data:image/png;base64,{encoded_image}"

    # Hacer HTML
    html_content = template.render(fecha=fecha_hoy, registros=registros, ruta_imagen=ruta_imagen_base64)

    # Generar PDF
    try:
        pdfkit.from_string(html_content, 'informe_temperaturas.pdf')
        print("PDF generado correctamente.")
    except Exception as e:
        print(f"Error al generar el PDF: {e}")

