import streamlit as st
from datetime import date

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Evaluación Técnica IMW", layout="wide")

# --- BASE DE DATOS DE PREGUNTAS (45) ---
# He mapeado cada pregunta con su inciso correcto según tu clave
preguntas_db = [
    {"id": 1, "p": "Durante el ensamble del conjunto bloque regulador de presión, ¿qué componente debe deslizar libremente antes de colocar el resorte?", "o": ["a) La válvula de retención", "b) El tapón NPT", "c) El pistón regulador", "d) El manómetro de presión"], "c": "c"},
    {"id": 2, "p": "Al armar la bomba de aceite, ¿cuál es el huelgo de rotación especificado entre los engranajes y el cuerpo?", "o": ["a) 0.008 a 0.009 pulgadas", "b) 0.003 a 0.004 pulgadas", "c) 0.0012 pulgadas", "d) 0.015 a 0.020 pulgadas"], "c": "b"},
    {"id": 3, "p": "¿Qué compuesto debe aplicarse a las roscas de los espárragos de los cilindros antes de su instalación definitiva?", "o": ["a) Locktite rojo", "b) Glyptol", "c) Aceite 55", "d) Antiaferrante"], "c": "d"},
    {"id": 4, "p": "En las bielas con lubricación interior, ¿cómo se asegura que el aceite llegue a la cruceta?", "o": ["a) Por salpicadura", "b) Conducto perforado en biela, buje y cruceta", "c) Tubería externa", "d) Seal carrier"], "c": "b"},
    {"id": 5, "p": "¿Cuál es el torque final para los espárragos de la guía de cruceta?", "o": ["a) 97 lbsf-ft (13.82 kgrf-m)", "b) 150 lbsf-ft", "c) 200 lbsf-ft", "d) 80 lbsf-ft"], "c": "a"},
    {"id": 6, "p": "Al ensamblar cilindros refrigerados por aire, ¿qué precaución se debe tener con las aletas?", "o": ["a) Cubrirlas con Glyptol", "b) Libres de pintura u obstrucciones", "c) Pintarlas negro brillante", "d) Lubricarlas"], "c": "b"},
    {"id": 7, "p": "¿Qué función cumple la junta de aluminio (gasket) en válvulas concéntricas?", "o": ["a) Sellado hermético por deformación", "b) Resorte de compensación", "c) Aislamiento eléctrico", "d) Lubricación"], "c": "a"},
    {"id": 8, "p": "¿Qué herramienta verifica que el cigüeñal no tenga huelgo axial excesivo?", "o": ["a) Cinta métrica", "b) Torquímetro", "c) Calibre estándar", "d) Comparador de caratula"], "c": "d"},
    {"id": 9, "p": "¿Por qué no usar llama directa para calentar rodamientos del cigüeñal?", "o": ["a) Consume oxígeno", "b) Altera tratamiento térmico del acero", "c) Genera grietas", "d) Dilata el eje"], "c": "b"},
    {"id": 10, "p": "¿Función de los 'shims' en la instalación del cigüeñal?", "o": ["a) Subir presión aceite", "b) Sellar fugas", "c) Ajustar huelgo axial total", "d) Reducir vibración"], "c": "c"},
    {"id": 11, "p": "¿Cómo deben quedar las aperturas de los anillos en el pistón?", "o": ["a) Alineadas verticalmente", "b) Escalonadas (no alineadas)", "c) Alineadas con el perno", "d) Cerradas con pega loca"], "c": "b"},
    {"id": 12, "p": "¿Qué verificar en las superficies de contacto del manifold?", "o": ["a) Acabado rugoso", "b) Capa de pintura", "c) Planicidad y sin rayas profundas", "d) Grasa de litio"], "c": "c"},
    {"id": 13, "p": "¿Para qué sirve el bulón perforado en la biela?", "o": ["a) Reducir peso", "b) Medir temperatura", "c) Ventilar gases", "d) Paso de aceite al perno"], "c": "d"},
    {"id": 14, "p": "¿Torque para tornillos de la tapa ciega del cárter?", "o": ["a) 150 lbsf-ft (20.73 kgrf-m)", "b) 200 lbsf-ft", "c) 100 lbsf-ft", "d) 50 lbsf-ft"], "c": "a"},
    {"id": 15, "p": "¿Qué usar para limpiar componentes antes del armado?", "o": ["a) Agua jabonosa", "b) Solventes limpios", "c) Gasolina con plomo", "d) Aire a presión"], "c": "b"},
    {"id": 16, "p": "Si engranajes de bomba de aceite no giran suavemente, ¿qué hacer?", "o": ["a) Forzar con llave", "b) Grasa pesada", "c) Desarmar y verificar suciedad", "d) Aplicar calor"], "c": "c"},
    {"id": 17, "p": "¿Referencia para posición de sellos de la empaquetadura (Seal Carrier)?", "o": ["a) Por el resorte", "b) Por el peso", "c) Por una flecha", "d) Por letras grabadas"], "c": "d"},
    {"id": 18, "p": "¿Qué pintura interna de cárter recomienda IMW?", "o": ["a) Rust-Oleum", "b) Behr Premium", "c) Glyptol", "d) Sayer"], "c": "c"},
    {"id": 19, "p": "¿Huelgo de dilatación del engranaje de bomba vs cigüeñal?", "o": ["a) 0.0012 in", "b) 0.008 in", "c) 0.003 in (0,075 mm)", "d) 0.005 in"], "c": "c"},
    {"id": 20, "p": "¿Hacia dónde orientar el chanfle del engranaje de lubricación?", "o": ["a) Extremo exterior", "b) Hacia la bomba", "c) Lado del contrapeso", "d) Indiferente"], "c": "c"},
    {"id": 21, "p": "¿Rango aceptable de huelgo total del cigüeñal?", "o": ["a) 0.003-0.004 in", "b) 0.008-0.009 in", "c) 0.005-0.007 in", "d) 0.010-0.012 in"], "c": "b"},
    {"id": 22, "p": "¿Lubricante recomendado para O-rings?", "o": ["a) Grasa litio", "b) Lubricante 55", "c) Antiaferrante", "d) Pasta roscas"], "c": "b"},
    {"id": 23, "p": "¿Torque para tornillos de las bielas?", "o": ["a) 150 lbsf-ft", "b) 80 lbsf-ft", "c) 100 lbsf-ft (13.82 kgrf-m)", "d) 200 lbsf-ft"], "c": "c"},
    {"id": 24, "p": "¿Hacia dónde deben apuntar las letras grabadas en caja de sellos?", "o": ["a) Al cigüeñal", "b) Al operario", "c) Abajo", "d) Al lado de presión"], "c": "d"},
    {"id": 25, "p": "¿Dónde queda el agujero de drenaje al montar guías de cruceta?", "o": ["a) Arriba", "b) Abajo", "c) Hacia la bomba", "d) Al manifold"], "c": "b"},
    {"id": 26, "p": "¿Tolerancia de huelgo entre cruceta y guía?", "o": ["a) 0.001 in", "b) 0.008 in", "c) 0.005 in", "d) 0.003 in"], "c": "c"},
    {"id": 27, "p": "¿Material de sellado para tapones NPT en cárter?", "o": ["a) Teflón", "b) Lock-tite verde", "c) Pasta para roscas", "d) Grasa Molikote"], "c": "c"},
    {"id": 28, "p": "¿Propósito de pintar paredes internas del cárter?", "o": ["a) Calor", "b) Sellar grietas", "c) Evitar desprendimiento partículas", "d) Flujo"], "c": "c"},
    {"id": 29, "p": "Transductor 4-20mA, R=250 Ohm, V=3.5V. ¿Corriente?", "o": ["a) 10 mA", "b) 12 mA", "c) 14 mA", "d) 16 mA"], "c": "c"},
    {"id": 30, "p": "¿Qué tipo de circuito es un sistema de paros de emergencia?", "o": ["a) Serie", "b) Paralelo", "c) Mixto", "d) Todas"], "c": "a"},
    {"id": 31, "p": "¿Herramientas para diagnosticar paros de emergencia?", "o": ["a) Amperímetro", "b) Multímetro y manual", "c) Óhmetro y manual", "d) Todas"], "c": "b"},
    {"id": 32, "p": "Carga 4.5A a 220V. Potencia y protección (125%):", "o": ["a) 990 W | 6 A", "b) 990 W | 10 A", "c) 1100 W | 10 A", "d) 450 W | 5 A"], "c": "a"},
    {"id": 33, "p": "ITM 1A dispara al activar solenoide 24VAC. ¿Causa probable?", "o": ["a) Voltaje alto", "b) Corto interno bobina", "c) Émbolo lubricado", "d) Tierra desconectada"], "c": "b"},
    {"id": 34, "p": "Flujo teórico 1400 m3/h, real 1234. ¿Eficiencia?", "o": ["a) 78.2%", "b) 84.5%", "c) 88.14%", "d) 92.3%"], "c": "c"},
    {"id": 35, "p": "1,500 m3 gas (0.74 kg/m3) a litros eq (0.72 kg/L):", "o": ["a) 1,110 L", "b) 1,458 L", "c) 1,541 L", "d) 2,027 L"], "c": "c"},
    {"id": 36, "p": "Sensor K errático junto a cable potencia. ¿Causa?", "o": ["a) Metales", "b) Inducción (ruido)", "c) Límite temp", "d) Polaridad"], "c": "b"},
    {"id": 37, "p": "Motor desconectado fases: 0.2, 0.2 e infinito. ¿Diagnóstico?", "o": ["a) Corto", "b) Bobina abierta", "c) Mal calibrado", "d) Desbalance"], "c": "b"},
    {"id": 38, "p": "Phase Loss pero hay 440V en entrada. ¿Qué revisar?", "o": ["a) Contactos ITM", "b) Fusible", "c) Sensor", "d) Ventilación"], "c": "a"},
    {"id": 39, "p": "Diferencia diagnóstico termopar J y K:", "o": ["a) Metales", "b) Color y rango", "c) Compensación", "d) Presión"], "c": "b"},
    {"id": 40, "p": "PLC Relay LED ON pero 0V en salida. ¿Falla?", "o": ["a) Programa", "b) Contacto interno dañado", "c) Presión", "d) Contraseña"], "c": "b"},
    {"id": 41, "p": "Sensor 4-20mA marca siempre 4mA fijo. ¿Prueba?", "o": ["a) Reset PLC", "b) Inyectar 12mA", "c) Aceite", "d) Continuidad"], "c": "b"},
    {"id": 42, "p": "Contactor con zumbido fuerte. ¿Mantenimiento?", "o": ["a) Limpiar caras polares y platinos", "b) Subir voltaje", "c) Pintar", "d) Sensor J"], "c": "a"},
    {"id": 43, "p": "Arrancador suave Current Limit bajo. ¿Síntoma?", "o": ["a) Giro inverso", "b) No vence inercia", "c) Presión alta", "d) Reset"], "c": "b"},
    {"id": 44, "p": "Relevador pegado sin energía. ¿Causa eléctrica?", "o": ["a) Arco / Microsoldadura", "b) Presión", "c) Frecuencia", "d) Cable K"], "c": "a"},
    {"id": 45, "p": "Guardamotor dispara por calor en tablero. ¿Causa?", "o": ["a) Altitud", "b) Temperatura afecta bimetales", "c) Descalibrado", "d) Humedad"], "c": "b"},
]

# --- LÓGICA DE INTERFAZ ---
with st.sidebar:
    st.header("Datos de Registro")
    nombre = st.text_input("Nombre del Técnico:")
    supervisor = st.selectbox("Supervisor Encargado:", ["Gerardo Lopez", "Eduardo Solano", "Joaquin Castillo", "Julian Garcia"])
    fecha_eval = st.date_input("Fecha:", date.today())

st.title(f"📋 Evaluación Técnica: {nombre if nombre else '---'}")
st.subheader("Sistemas de Compresión y Control GNC")

respuestas_usuario = {}

# Mostrar preguntas con formato A, B, C, D
for item in preguntas_db:
    st.markdown(f"### {item['id']}. {item['p']}")
    # Usamos el inciso inicial para la comparación
    seleccion = st.radio("Seleccione una opción:", item['o'], key=item['id'], index=None)
    if seleccion:
        respuestas_usuario[item['id']] = seleccion[0] # Guarda solo la letra 'a', 'b', etc.
    st.write("---")

st.subheader("Sección de Análisis Abierto")
ans_46 = st.text_area("46. Describa la función del Panel de Prioridad y su lógica de flujo:")
ans_47 = st.text_area("47. Caso Práctico: Banco de Alta estancado a 2800 PSI. Diagnóstico:")

if st.button("Finalizar y Calificar"):
    if not nombre:
        st.error("Por favor, ingrese el nombre del técnico.")
    else:
        aciertos = 0
        for item in preguntas_db:
            if item['id'] in respuestas_usuario:
                if respuestas_usuario[item['id']] == item['c']:
                    aciertos += 1
        
        pct = (aciertos / len(preguntas_db)) * 100
        
        # Umbrales solicitados por el usuario
        if pct <= 60:
            status, color = "REPROBADO", "red"
        elif pct <= 85:
            status, color = "APROBADO", "orange"
        else:
            status, color = "EXCELENTE", "green"

        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Aciertos", f"{aciertos} / {len(preguntas_db)}")
        c2.metric("Puntaje Final", f"{pct:.1f}%")
        c3.markdown(f"### Estatus: <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
        
        st.download_button("Guardar Reporte", 
                           f"Técnico: {nombre}\nResultado: {pct:.1f}%\nEstatus: {status}\nSupervisor: {supervisor}", 
                           file_name=f"Resultado_{nombre}.txt")