import streamlit as st
from datetime import date
from fpdf import FPDF

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Sistema de Evaluación Técnica IMW", layout="wide")

# --- FUNCIÓN PARA GENERAR PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Reporte de Evaluación Técnica - GNC', 0, 1, 'C')
        self.ln(5)

def generar_pdf(nombre, supervisor, fecha, aciertos, total, porcentaje, status, r46, r47):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Datos de cabecera
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, f"DATOS GENERALES", 1, 1, 'C', 1)
    pdf.cell(95, 10, f"Técnico: {nombre}", 1)
    pdf.cell(95, 10, f"Fecha: {fecha}", 1, 1)
    pdf.cell(0, 10, f"Supervisor: {supervisor}", 1, 1)
    pdf.ln(5)
    
    # Resultados
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 10, f"RESULTADOS DE LA EVALUACIÓN", 1, 1, 'C', 1)
    pdf.cell(63, 10, f"Aciertos: {aciertos}/{total}", 1)
    pdf.cell(63, 10, f"Puntaje: {porcentaje:.1f}%", 1)
    pdf.cell(64, 10, f"Estatus: {status}", 1, 1)
    pdf.ln(10)
    
    # Respuestas abiertas
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Respuestas de Análisis:", 0, 1)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, f"46. Panel de Prioridad: {r46}")
    pdf.ln(2)
    pdf.multi_cell(0, 10, f"47. Caso Estación Obrera: {r47}")
    
    return pdf.output(dest='S').encode('latin-1')

# --- BASE DE DATOS DE PREGUNTAS ---
preguntas_db = [
    # MECÁNICA (Ejemplos con contexto)
    {"id": 1, "p": "Durante el ensamble del conjunto bloque regulador de presión, ¿qué componente debe deslizar libremente antes de colocar el resorte?", "o": ["a) La válvula de retención", "b) El tapón NPT", "c) El pistón regulador", "d) El manómetro de presión"], "c": "c"},
    {"id": 16, "p": "Si los engranajes de la bomba de aceite no giran suavemente a mano durante el armado, ¿Qué se debe hacer?", "o": ["a) Forzar con llave", "b) Aplicar grasa", "c) Desarmar y verificar suciedad o rebabas", "d) Aplicar calor"], "c": "c"},
    {"id": 20, "p": "¿Hacia dónde debe orientarse el chanfle del engranaje de la bomba de lubricación?", "o": ["a) Extremo exterior", "b) Hacia la bomba", "c) Lado del contrapeso del cigüeñal", "d) Indiferente"], "c": "c"},
    {"id": 21, "p": "¿Rango aceptable de huelgo axial del cigüeñal?", "o": ["a) 0.003-0.004 in", "b) 0.008 a 0.009 pulgadas", "c) 0.015-0.020 in", "d) 0.005-0.007 in"], "c": "b"},
    
    # INSTRUMENTACIÓN Y CÁLCULOS
    {"id": 29, "p": "Lazo 4-20 mA con R=250 Ohm. Si el multímetro en paralelo marca 3.5 V, ¿Cuál es la intensidad de corriente?", "o": ["a) 10 mA", "b) 12 mA", "c) 14 mA", "d) 16 mA"], "c": "c"},
    {"id": 31, "p": "Para diagnosticar una falla en un circuito de paros de emergencia, ¿qué herramientas son útiles?", "o": ["a) Amperímetro", "b) Multímetro y manual de diagramas", "c) Óhmetro y manual", "d) Solo pinza voltiamperimétrica"], "c": "b"},
    {"id": 32, "p": "Resistencia a 220 VAC consume 4.5 A. ¿Potencia y capacidad del ITM (Factor 125%)?", "o": ["a) 990 W | 6 A", "b) 990 W | 10 A", "c) 1100 W | 10 A", "d) 450 W | 5 A"], "c": "a"},
    {"id": 33, "p": "ITM de 1 A dispara inmediatamente al activar solenoide de 24 VAC. ¿Causa más probable?", "o": ["a) Voltaje alto", "b) Cortocircuito interno en bobina", "c) Émbolo lubricado", "d) Falta de tierra"], "c": "b"},
    {"id": 34, "p": "Rendimiento: Flujo teórico 1400 m3/h, real 1234 m3/h. ¿Eficiencia volumétrica?", "o": ["a) 78.2%", "b) 84.5%", "c) 88.14%", "d) 92.3%"], "c": "c"},
    {"id": 35, "p": "Convertir 1,500 m3 gas (Dens. 0.74 kg/m3) a litros eq (Ref 0.72 kg/L):", "o": ["a) 1,110 L", "b) 1,458 L", "c) 1,541 L", "d) 2,027 L"], "c": "c"},
    
    # CONTROL Y FALLAS
    {"id": 36, "p": "Sensor tipo K con lecturas erráticas pasando junto a cable de potencia. ¿Causa probable?", "o": ["a) Metales", "b) Inducción electromagnética (Ruido)", "c) Límite temp", "d) Polaridad"], "c": "b"},
    {"id": 37, "p": "Motor desconectado: Resistencia entre fases 0.2, 0.2 e infinito. ¿Diagnóstico?", "o": ["a) Corto", "b) Bobina abierta", "c) Normal", "d) Desbalance"], "c": "b"},
    {"id": 38, "p": "Phase Loss en arrancador, pero hay 440V en entrada del ITM. ¿Revisar primero?", "o": ["a) Contactos ITM", "b) Fusible", "c) Sensor", "d) Ventilación"], "c": "a"},
    {"id": 39, "p": "¿Diferencia principal entre termopar Tipo J y Tipo K?", "o": ["a) Metales", "b) Color de código y rango", "c) Compensación", "d) Presión"], "c": "b"},
    {"id": 40, "p": "PLC Relay LED ON pero salida marca 0V. ¿Falla probable?", "o": ["a) Programa", "b) Contacto interno dañado", "c) Presión", "d) Bloqueo"], "c": "b"},
    {"id": 41, "p": "Sensor 4-20mA marca siempre 4mA fijo. ¿Prueba para descartar PLC?", "o": ["a) Reset", "b) Inyectar 12mA al canal", "c) Aceite", "d) Continuidad"], "c": "b"},
    {"id": 42, "p": "Contactor con zumbido fuerte. ¿Mantenimiento correctivo?", "o": ["a) Limpiar caras polares y platinos", "b) Subir voltaje", "c) Pintar", "d) Sensor J"], "c": "a"},
    {"id": 43, "p": "Arrancador suave con Current Limit muy bajo. ¿Síntoma?", "o": ["a) Giro inverso", "b) No vence inercia de arranque", "c) Presión alta", "d) Reset"], "c": "b"},
    {"id": 44, "p": "Relevador pegado sin energía en bobina. ¿Causa eléctrica?", "o": ["a) Arco / Microsoldadura de contactos", "b) Presión", "c) Frecuencia", "d) Cable K"], "c": "a"},
    {"id": 45, "p": "Guardamotor dispara por sobrecarga durante horas de calor ambiental intenso. ¿Causa?", "o": ["a) Altitud", "b) Temperatura ambiental afecta bimetales", "c) Calibración", "d) Humedad"], "c": "b"},
]

# --- INTERFAZ ---
with st.sidebar:
    st.header("Datos de Registro")
    nombre = st.text_input("Nombre del Técnico:")
    supervisor = st.selectbox("Supervisor Encargado:", ["Gerardo Lopez", "Eduardo Solano", "Joaquin Castillo", "Julian Garcia"])
    fecha_eval = st.date_input("Fecha:", date.today())

st.title(f"📋 Evaluación Técnica: {nombre if nombre else '---'}")
st.subheader("Sistemas de Compresión y Control GNC (IMW)")

respuestas_usuario = {}

# Mostrar preguntas
st.header("I. Evaluación de Conocimientos Técnicos")
for item in preguntas_db:
    st.markdown(f"**{item['id']}. {item['p']}**")
    sel = st.radio("Seleccione una opción:", item['o'], key=item['id'], index=None)
    if sel: respuestas_usuario[item['id']] = sel[0]
    st.write("---")

st.header("II. Análisis de Casos Reales")
ans_46 = st.text_area("46. Describa la función del Panel de Prioridad y su lógica de flujo:")
ans_47 = st.text_area("47. Caso Estación Obrera: Banco de Alta estancado en 2800 PSI. Diagnóstico técnico:")

if st.button("Finalizar y Generar Certificado PDF"):
    if not nombre:
        st.error("Por favor, ingrese el nombre del evaluado.")
    else:
        aciertos = sum(1 for q in preguntas_db if q['id'] in respuestas_usuario and respuestas_usuario[q['id']] == q['c'])
        pct = (aciertos / len(preguntas_db)) * 100
        
        status = "REPROBADO"
        if pct >= 85: status = "EXCELENTE / APROBADO"
        elif pct >= 70: status = "APROBADO"

        # Generar PDF
        pdf_data = generar_pdf(nombre, supervisor, fecha_eval, aciertos, len(preguntas_db), pct, status, ans_46, ans_47)
        
        st.success(f"Evaluación terminada. Puntaje: {pct:.1f}%")
        st.download_button(label="⬇️ Descargar Resultados (PDF No Editable)", 
                           data=pdf_data, 
                           file_name=f"Resultado_{nombre}.pdf", 
                           mime="application/pdf")
