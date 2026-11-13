"""Genera el PDF a partir de las capturas y respuestas HTTP reales."""
import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Preformatted

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'entrega'
OUT.mkdir(exist_ok=True)
data = json.loads((ROOT / 'evidencia/pruebas-capturadas.json').read_text(encoding='utf-8'))
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleCustom', fontName='Helvetica-Bold', fontSize=32, leading=38, textColor=colors.HexColor('#153854'), spaceAfter=20))
styles.add(ParagraphStyle(name='SubCustom', fontSize=12, leading=18, textColor=colors.HexColor('#426580'), spaceAfter=12))
styles.add(ParagraphStyle(name='BodyCustom', fontSize=11, leading=17, spaceAfter=12))
styles.add(ParagraphStyle(name='CodeCustom', fontName='Courier', fontSize=7.4, leading=11, backColor=colors.HexColor('#eef3f7'), borderPadding=9))
story = []
def p(text, style='BodyCustom'):
    story.append(Paragraph(text, styles[style]))

story.append(Spacer(1, 68))
p('DESARROLLO WEB / EXAMEN FINAL', 'SubCustom')
p('Serie 4<br/>API REST de Vehículos', 'TitleCustom')
p('Django REST Framework + MySQL', 'SubCustom')
story.append(Spacer(1, 34))
p('<b>Estudiante:</b> Fritz Ian Valentino Urizar Rodas<br/><b>Carné:</b> 3090-22-8199<br/><b>Fecha:</b> 12 de noviembre de 2026')
p('<b>Recurso elegido:</b> Vehículos.<br/><b>Herramienta de pruebas:</b> cliente HTTP local incluido en el proyecto, ejecutado en Microsoft Edge mediante Playwright.')
p('API local: http://127.0.0.1:8000/api/vehiculos/')
p('Repositorio: <link href="https://github.com/Iantino/Examen-Final-Desarrollo-Web" color="#164f83">github.com/Iantino/Examen-Final-Desarrollo-Web</link>')
p('Implementación sin autenticación, conforme al enunciado. Incluye operaciones para crear, listar, consultar por ID, actualizar y eliminar; respuestas JSON y validación de campos obligatorios.')
p('<b>Modelo:</b> id, marca, modelo, anio, color, created_at y updated_at. Los campos de texto no aceptan valores vacíos. El año debe estar entre 1886 y el próximo año. Las fechas son administradas por Django.')
story.append(PageBreak())

explanations = [
 'El POST válido crea un registro en MySQL. Devuelve el identificador y las fechas administradas por Django con estado 201 Created.',
 'El GET devuelve una lista JSON. Se observa el registro creado en la prueba anterior y sus siete campos; estado 200 OK.',
 'El GET con el identificador generado devuelve únicamente ese vehículo; estado 200 OK. Un identificador inexistente responde 404.',
 'El PUT envía los cuatro atributos y cambia el color de Blanco a Azul. La respuesta conserva el ID y created_at, y actualiza updated_at; estado 200 OK.',
 'El POST inválido envía marca vacía, un año anterior a 1886 y omite modelo y color. Devuelve errores por campo y estado 400 Bad Request; no crea un registro.',
 'El DELETE elimina el registro creado durante las pruebas. Devuelve 204 No Content, por lo que no contiene cuerpo JSON. Una consulta posterior al mismo ID devolvió 404 y confirmó la eliminación.',
]
for index, (item, explanation) in enumerate(zip(data, explanations), 1):
    p(f'PRUEBA {index} / 6', 'SubCustom')
    p(escape(item['titulo'][3:]), 'TitleCustom')
    p(f"<b>{item['metodo']}</b> {escape(item['url'])}<br/><b>Estado comprobado:</b> {item['estado']}")
    p(explanation)
    image_path = ROOT / f'evidencia/{index:02}.png'
    story.append(Image(str(image_path), width=499, height=499 * 950 / 1280))
    story.append(Spacer(1, 15))
    p('Captura real del cliente HTTP: método, URL, cuerpo enviado y respuesta del servidor. El archivo evidencia/pruebas-capturadas.json conserva los datos originales.', 'SubCustom')
    story.append(PageBreak())

p('INCISO B / CONSUMO CON REACT', 'SubCustom')
p('Mostrar la lista de vehículos', 'TitleCustom')
p('<b>useState:</b> mantiene la lista de vehículos y el mensaje de error. La lista comienza vacía; al recibir el JSON, setVehiculos actualiza el estado y React vuelve a renderizar el componente.')
p('<b>useEffect:</b> ejecuta la consulta al montar el componente mediante el arreglo de dependencias vacío. Su limpieza cancela la solicitud al desmontar para evitar procesar una respuesta que ya no se necesita.')
p('<b>fetch:</b> envía GET a la URL local real de la API. Comprueba r.ok antes de convertir la respuesta JSON. Si falla la red o el estado HTTP, muestra un mensaje de error; una cancelación no se presenta como fallo.')
p('<b>map y key:</b> map transforma cada vehículo en un elemento li con marca, modelo, año y color. key={v.id} permite a React reconocer cada elemento de forma estable, incluso cuando cambia la lista.')
p('<b>Fragmento de código (15 líneas):</b>')
code = (ROOT / 'react/Vehiculos.jsx').read_text(encoding='utf-8').rstrip()
assert len(code.splitlines()) <= 15
story.append(Preformatted(code, styles['CodeCustom']))
story.append(Spacer(1, 18))
p('El servidor debe estar activo en 127.0.0.1:8000. El componente debe integrarse en una aplicación React servida desde el mismo origen o con un proxy; si se usa otro origen, se debe configurar CORS. GitHub almacena el código y no hospeda esta API ni su base de datos.')
p('Referencias: docs.djangoproject.com/en/5.2/ref/databases/ y www.django-rest-framework.org/api-guide/serializers/', 'SubCustom')

def footer(canvas, doc):
    canvas.setStrokeColor(colors.HexColor('#ccd8e3'))
    canvas.line(48, 44, A4[0] - 48, 44)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#527086'))
    canvas.drawString(48, 30, 'Serie 4 - Vehículos | Fritz Ian Valentino Urizar Rodas')
    canvas.drawRightString(A4[0]-48, 30, str(doc.page))

doc = SimpleDocTemplate(str(OUT / 'Serie4_Vehiculos.pdf'), pagesize=A4,
    rightMargin=48, leftMargin=48, topMargin=44, bottomMargin=62,
    title='Serie 4 - API REST de Vehículos', author='Fritz Ian Valentino Urizar Rodas')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT / 'Serie4_Vehiculos.pdf')
