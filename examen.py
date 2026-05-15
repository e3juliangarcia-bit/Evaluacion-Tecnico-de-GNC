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
    pdf.set_font("Arial", size=11)
    
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
    
    # Respuestas de texto
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "Respuestas de Análisis Abierto:", 0, 1)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, f"46. Función Panel de Prioridad: \n{r46}")
    pdf.ln(4)
    pdf.multi_cell(0, 8, f"47. Caso Estación Obrera: \n{r47}")
    
    return pdf.output(dest='S').encode('latin-1')

# --- BASE DE DATOS DE PREGUNTAS (1 a 45) ---
preguntas_db = [
    {"id": 1, "p": "Durante el ensamble del conjunto bloque regulador de presión (bloque del filtro de aceite), ¿qué componente debe deslizar libremente antes de colocar el resorte?", "o": ["a) La válvula de retención", "b) El tapón NPT", "c) El pistón regulador", "d) El manómetro de presión"], "c": "c"},
    {"id": 2, "p": "Al armar la bomba de aceite, ¿cuál es el huelgo de rotación especificado entre los engranajes y el cuerpo?", "o": ["a) 0.008 a 0.009 pulgadas", "b) 0.003 a 0.004 pulgadas", "c) 0.0012 pulgadas", "d) 0.015 a 0.020 pulgadas"], "c": "b"},
    {"id": 3, "p": "¿Qué compuesto debe aplicarse a las roscas de los espárragos de los cilindros antes de su instalación definitiva?", "o": ["a) Locktite rojo", "b) Glyptol", "c) Aceite 55", "d) Antiaferrante"], "c": "d"},
    {"id": 4, "p": "En las bielas con lubricación interior, ¿cómo se asegura que el aceite llegue a la cruceta?", "o": ["a) Mediante salpicadura desde el cárter generada por el giro del cigüeñal", "b) A través de un conducto perforado en el cuerpo de la biela, buje y cruceta", "c) Por el sistema de tubería externa de lubricación, conectado desde el bloque regulador de presión de aceite hasta la guía", "d) A través del sello de aceite del seal carrier"], "c": "b"},
    {"id": 5, "p": "¿Cuál es el torque final para los espárragos de la guía de cruceta?", "o": ["a) 97 lbsf-ft (13.82 kgrf-m)", "b) 150 lbsf-ft (20,73 kgrf-m)", "c) 200 lbsf-ft (27,64 kgrf-m)", "d) 80 lbsf-ft (11.06 kgrf-m)"], "c": "a"},
    {"id": 6, "p": "Al ensamblar cilindros refrigerados por aire, ¿qué precaución se debe tener con las aletas de enfriamiento?", "o": ["a) Cubrirlas con una capa gruesa de Glyptol", "b) Asegurar que estén libres de pintura u obstrucciones", "c) Pintarlas de color negro brillante", "d) Lubricarlas con Aceite 55"], "c": "b"},
    {"id": 7, "p": "En el sistema de válvulas concéntricas, ¿qué función cumple la junta de aluminio (gasket)?", "o": ["a) Proporcionar un sellado hermético por deformación controlada", "b) Actuar como un resorte de compensación", "c) Aislar eléctricamente la válvula del bloque", "d) Lubricar el asiento de la válvula"], "c": "a"},
    {"id": 8, "p": "¿Qué herramienta se utiliza para verificar que el cigüeñal no tenga huelgo axial excesivo?", "o": ["a) Cinta métrica", "b) Torquímetro", "c) Calibre (Pie de rey) estándar", "d) Comparador de caratula"], "c": "d"},
    {"id": 9, "p": "Durante el montaje de los rodamientos del cigüeñal, ¿por qué no se debe usar llama directa para calentarlos?", "o": ["a) Porque la llama consume el oxígeno necesario causando corrosión", "b) Porque puede alterar el tratamiento térmico del acero", "c) Porque se generan grietas en las crestas del engranaje", "d) Porque dilata el eje en lugar del rodamiento"], "c": "b"},
    {"id": 10, "p": "¿Cuál es la función de los 'shims' en la instalación del cigüeñal en el bloque del cárter?", "o": ["a) Aumentar la presión de aceite", "b) Sellar fugas de aceite externas", "c) Ajustar el huelgo axial total del cigüeñal", "d) Reducir la vibración del motor"], "c": "c"},
    {"id": 11, "p": "Al instalar los anillos en el pistón, ¿cómo deben quedar posicionadas las aperturas?", "o": ["a) Todas alineadas en una sola línea vertical", "b) Escalonadas (no alineadas entre sí)", "c) Alineadas con el perno del pistón", "d) Cerradas completamente mediante pega loca"], "c": "b"},
    {"id": 12, "p": "En el ensamblado del manifold (porta válvulas), ¿qué se debe verificar en las superficies de contacto?", "o": ["a) Que tengan un acabado rugoso para evitar el deslizamiento", "b) Que estén cubiertas de una capa de pintura especifica", "c) Planicidad y ausencia de rayas profundas", "d) Que estén lubricadas con grasa de litio"], "c": "c"},
    {"id": 13, "p": "¿Para qué sirve el bulón perforado en el conjunto de la biela?", "o": ["a) Para reducir el peso total del conjunto", "b) Para medir la temperatura interna del aceite", "c) Para ventilar los gases del cárter", "d) Para permitir el paso de aceite hacia el perno de la biela"], "c": "d"},
    {"id": 14, "p": "Al montar la tapa ciega del cárter, ¿cuál es el torque especificado para sus tornillos?", "o": ["a) 150 lbsf-ft (20.73 kgrf-m)", "b) 200 lbsf-ft (27.64 kgrf-m)", "c) 100 lbsf-ft (13.82 kgrf-m)", "d) 50 lbsf-ft (6.91 kgrf-m)"], "c": "a"},
    {"id": 15, "p": "¿Qué se debe usar para limpiar los componentes del compresor antes del armado final?", "o": ["a) Agua jabonosa", "b) Solventes limpios", "c) Gasolina con plomo", "d) Aire a presión solamente"], "c": "b"},
    {"id": 16, "p": "16. Si los engranajes de la bomba de aceite no giran suavemente a mano, ¿qué se debe hacer?", "o": ["a) Aplicar lubricante WD-40 y forzarlos con una llave hasta que cedan", "b) Llenar la bomba con grasa pesada", "c) Desarmar y verificar interferencias o suciedad", "d) Aplicar calor para dilatar el cuerpo"], "c": "c"},
    {"id": 17, "p": "¿Qué se toma como referencia para la correcta posición de los sellos de la caja de empaquetadura (seal Carrier)?", "o": ["a) Por la posición y forma del resorte", "b) Por el peso de la pieza", "c) Por una flecha pintada con marcador", "d) Por las letras grabadas en el sello"], "c": "d"},
    {"id": 18, "p": "¿Qué pintura para recubrimiento de las paredes internas del cárter recomienda usar IMW en los equipos?", "o": ["a) Rust-Oleum", "b) Behr Premium", "c) Glyptol", "d) Sayer"], "c": "c"},
    {"id": 19, "p": "¿A qué huelgo de dilatación debe llegar el engranaje de la bomba de aceite, con respecto al diámetro de muñón del cigüeñal, antes de ser instalado?", "o": ["a) 0.0012 pulgadas (0,03 mm)", "b) 0.008 pulgadas (0.203 mm)", "c) 0.003 pulgadas (0,075 mm)", "d) 0.005 pulgadas (0,127 mm)"], "c": "c"},
    {"id": 20, "p": "20. ¿Hacia dónde debe orientarse el chanfle del engranaje de la bomba de lubricación?", "o": ["a) Hacia el extremo exterior del cigüeñal", "b) Hacia la bomba de aceite", "c) Hacia el lado del contrapeso", "d) Es indiferente"], "c": "c"},
    {"id": 21, "p": "21. Durante el ajuste del huelgo total del cigüeñal, ¿cuál es el rango aceptable?", "o": ["a) 0.003 a 0.004 pulgadas", "b) 0.008 a 0.009 pulgadas", "c) 0.005 a 0.007 pulgadas", "d) 0.010 a 0.012 pulgadas"], "c": "b"},
    {"id": 22, "p": "¿Qué lubricante se recomienda para los O-rings?", "o": ["a) Grasa de litio", "b) Lubricante 55", "c) Antiaferrante", "d) Pasta para roscas"], "c": "b"},
    {"id": 23, "p": "¿Cuál es el torque de apriete requerido para los tornillos de las bielas?", "o": ["a) 150 lbsf-ft (20.73 kgrf-m)", "b) 80 lbsf-ft (11 kgrf-m)", "c) 100 lbsf-ft (13,82 kgrf-m)", "d) 200 lbsf-ft (27.64 kgrf-m)"], "c": "c"},
    {"id": 24, "p": "En la caja de sellos, ¿hacia dónde deben apuntar las letras grabadas?", "o": ["a) Hacia el cigüeñal", "b) Hacia el operario", "c) Hacia abajo para drenaje", "d) Hacia el lado de la presión (lejos del block)"], "c": "d"},
    {"id": 25, "p": "Al montar las guías de cruceta, ¿dónde debe quedar el agujero de drenaje?", "o": ["a) Hacia arriba", "b) Hacia abajo", "c) Hacia la bomba de aceite", "d) Hacia el manifold"], "c": "b"},
    {"id": 26, "p": "¿Cuál es la tolerancia de huelgo requerida entre la cruceta y su guía?", "o": ["a) 0.001 pulgadas", "b) 0.008 pulgadas", "c) 0.005 pulgadas", "d) 0.003 pulgadas"], "c": "c"},
    {"id": 27, "p": "Para los tapones NPT ubicados en el cárter, ¿qué material de sellado se usa?", "o": ["a) Cinta de Teflón", "b) Lock-tite verde", "c) Pasta para roscas", "d) Grasa Molikote"], "c": "c"},
    {"id": 28, "p": "¿Cuál es el propósito de pintar las paredes internas del cárter?", "o": ["a) Mejorar la disipación de calor", "b) Sellar grietas estructurales", "c) Evitar que partículas de la fundición se desprendan", "d) Facilitar el flujo de aceite"], "c": "c"},
    {"id": 29, "p": "29. Se está realizando el diagnóstico de un lazo de control de un transductor de presión que opera con una señal de 4 - 20 mA. Para medir la caída de tensión y verificar la señal con un multímetro, se utiliza una resistencia de precisión de 250 Ohm en el lazo. Si el multímetro conectado en paralelo a la resistencia de 250 Ohm marca una lectura de 3.5 V, ¿cuál es la intensidad de corriente que circula por el lazo en ese momento?", "o": ["a) 10 mA", "b) 12 mA", "c) 14 mA", "d) 16 mA"], "c": "c"},
    {"id": 30, "p": "30. ¿En el sistema de control de los equipos IMW, qué tipo de circuito eléctrico, es un circuito de paros de emergencia?", "o": ["a) Circuito serie.", "b) Circuito paralelo.", "c) Circuito mixto.", "d) Todas las anteriores."], "c": "a"},
    {"id": 31, "p": "31. Para diagnosticar una falla en un circuito de paros de emergencia, cuales de las siguientes herramientas son útiles para tal propósito:", "o": ["a) Amperímetro y caza fallas.", "b) Multímetro y manual eléctrico de equipo.", "c) Óhmetro y manual eléctrico de equipo.", "d) Todas las anteriores."], "c": "b"},
    {"id": 32, "p": "32. Durante el mantenimiento preventivo de un tablero de control, se identifica una resistencia que opera a una tensión de 220 VAC. Al realizar la medición con una pinza amperimétrica, se obtiene una lectura de consumo de 4.5 A. ¿Cuál es la potencia eléctrica que está disipando la resistencia y qué capacidad mínima debería tener el interruptor termomagnético de protección (considerando un factor de seguridad del 125%, según estándares de ingeniería)?", "o": ["a) 990 W | Protección de 6 A", "b) 990 W | Protección de 10 A", "c) 1100 W | Protección de 10 A", "d) 450 W | Protección de 5 A"], "c": "a"},
    {"id": 33, "p": "33. Un interruptor termomagnético de 1 A que protege una válvula solenoide de 24 VAC se dispara inmediatamente al activar la señal de apertura. ¿Cuál es la causa más probable de la falla?", "o": ["a) El voltaje de la fuente es superior a 24 VAC.", "b) La bobina de la solenoide presenta una pérdida de aislamiento (cortocircuito interno).", "c) El émbolo de la válvula está ligeramente lubricado.", "d) El cable de tierra física está desconectado."], "c": "b"},
    {"id": 34, "p": "34. En una estación de GNC, se requiere validar el rendimiento de un compresor. Según la placa del fabricante, el equipo tiene un flujo teórico de 1400 m3/h. Al realizar una medición real mediante la ERM, el flujo registrado es de 1234 m3/h. ¿Cuál es la eficiencia volumétrica actual del compresor (nv)?", "o": ["a) 78.2%", "b) 84.5%", "c) 88.14%", "d) 92.3%"], "c": "c"},
    {"id": 35, "p": "35. Un módulo de almacenamiento transportable (MAT) ha descargado un volumen total de 1,500 m3 de gas natural en una estación de servicio. Para fines de control de venta y comparación de consumo, se requiere convertir este volumen a litros equivalentes. Datos técnicos: • Densidad del gas natural en el sitio: 0.74 kg/m3 • Densidad de referencia del combustible líquido: 0.72 kg/L. ¿A cuántos litros equivalentes corresponde el volumen de gas descargado por el MAT?", "o": ["a) 1,110 Litros", "b) 1,458 Litros", "c) 1,541 Litros", "d) 2,027 Litros"], "c": "c"},
    {"id": 36, "p": "36. Un sensor de temperatura tipo K muestra lecturas erráticas en el HMI del compresor. Al revisar, notas que el cable del sensor está pasando junto a un cable de potencia del motor. ¿Cuál es la causa más probable?", "o": ["a) Incompatibilidad de metales en la unión.", "b) Interferencia por inducción electromagnética (ruido).", "c) El sensor ha superado su límite de temperatura.", "d) Inversión de polaridad en el PLC."], "c": "b"},
    {"id": 37, "p": "37. Durante un arranque, el guardamotor se dispara instantáneamente. Al medir la resistencia entre las fases del motor (desconectado), obtienes 0.2 Ohms, 0.2 Ohms e infinito. ¿Qué indica este diagnóstico?", "o": ["a) El motor está en cortocircuito.", "b) Una de las bobinas del motor está abierta.", "c) El guardamotor está mal calibrado.", "d) Desbalance de voltajes en la red."], "c": "b"},
    {"id": 38, "p": "38. Un arrancador suave muestra la falla perdida de fase (Phase Loss), pero el voltímetro en la entrada del ITM indica 440 V entre todas las fases. ¿Qué componente intermedio deberías revisar primero?", "o": ["a) Los contactos principales del ITM.", "b) El fusible del transformador de control.", "c) El sensor de presión de succión.", "d) La ventilación del tablero."], "c": "a"},
    {"id": 39, "p": "39. ¿Cuál es la diferencia principal en el diagnóstico entre un termopar Tipo J y uno Tipo K?", "o": ["a) El Tipo J usa cables de cobre y el K de plata.", "b) El código de colores y el rango de temperatura.", "c) El Tipo K no necesita cable de compensación.", "d) El Tipo J es solo para presiones altas."], "c": "b"},
    {"id": 40, "p": "40. Un PLC tiene una salida digital tipo relevador (Relay) activada (LED encendido), pero la electroválvula no se energiza. Al medir el voltaje en el terminal de salida del PLC obtienes 0 V. ¿Cuál es la falla más probable?", "o": ["a) El programa del PLC tiene un error.", "b) El contacto interno del relevador del PLC está dañado o quemado.", "c) La válvula tiene mucha presión de gas.", "d) Falta la contraseña del HMI."], "c": "b"},
    {"id": 41, "p": "41. En un sistema con PLC, detectas que un sensor de presión de 4 - 20 mA marca siempre el valor mínimo 4 mA, sin importar el cambio de presión real. ¿Qué prueba realizarías para descartar el PLC?", "o": ["a) Reiniciar el PLC a valores de fábrica.", "b) Inyectar una señal de 12 mA con un calibrador de procesos o fuente de generación de corriente.", "c) Cambiar el aceite del compresor.", "d) Medir continuidad en la alimentación de AC."], "c": "b"},
    {"id": 42, "p": "42. Un contactor de motor hace un ruido fuerte (zumbido) al activarse. ¿Qué mantenimiento preventivo corregiría esto?", "o": ["a) Limpiar las caras polares del núcleo magnético de polvo o grasa y los platinos de los contactos.", "b) Aumentar el voltaje de la bobina por encima de lo nominal.", "c) Pintar la carcasa del contactor.", "d) Sustituir el sensor de temperatura tipo J."], "c": "a"},
    {"id": 43, "p": "43. Al configurar un arrancador suave para un compresor, el técnico establece un límite de corriente (Current Limit) muy bajo. ¿Qué síntoma presentará el equipo?", "o": ["a) El motor girará en sentido contrario.", "b) El motor no logrará vencer la inercia y el arrancador se alarmará.", "c) La presión de descarga subirá instantáneamente.", "d) El PLC se reiniciará automáticamente."], "c": "b"},
    {"id": 44, "p": "44. Un relevador de control se queda pegado (no abre el contacto al quitar energía a la bobina). Tras descartar falla mecánica, ¿qué fenómeno eléctrico podría ser la causa?", "o": ["a) Magnetismo remanente o micro soldadura por arco eléctrico.", "b) Exceso de presión en la línea de gas.", "c) Baja frecuencia en el generador Cummins.", "d) Uso de cable de compensación tipo K."], "c": "a"},
    {"id": 45, "p": "45. Un guardamotor está configurado a 10 A para un motor que consume 9 A. Si el motor se dispara frecuentemente por 'Sobre carga en motor' durante las horas de más calor, ¿cuál es la causa más probable?", "o": ["a) La altitud de la zona afecta el magnetismo.", "b) Temperatura ambiente elevada en el tablero que afecta los bimetales.", "c) El sensor de presión está descalibrado.", "d) Falla en el PLC por humedad."], "c": "b"},
]

# --- INTERFAZ ---
with st.sidebar:
    st.header("Datos de Registro")
    nombre = st.text_input("Nombre del Técnico:")
    supervisor = st.selectbox("Supervisor Encargado:", ["Gerardo Lopez", "Eduardo Solano", "Joaquin Castillo", "Julian Garcia"])
    fecha_eval = st.date_input("Fecha:", date.today())

st.title(f"📋 Evaluación Técnica IMW: {nombre if nombre else '---'}")
st.subheader("Cuestionario de Conocimientos GNC e Instrumentación")

respuestas_usuario = {}

# Mostrar las 45 preguntas
for item in preguntas_db:
    st.markdown(f"### {item['p']}")
    sel = st.radio("Seleccione la respuesta correcta:", item['o'], key=item['id'], index=None)
    if sel:
        respuestas_usuario[item['id']] = sel[0]
    st.write("---")

# Sección de Análisis Abierto
st.header("II. Sección de Análisis Detallado")

st.markdown("### 46. Función y Lógica del Panel de Prioridad")
ans_46 = st.text_area("Describa detalladamente la función de un Panel de Prioridad en una estación de GNC de tres líneas y la lógica de flujo hacia los bancos (Bajo, Medio y Alto):")

st.markdown("---")

st.markdown("### 47. Caso Práctico: Estación Obrera")
st.info("""El compresor alcanza su presión de paro nominal (3,600 PSI). Los Bancos de Baja y Medio están llenos, pero el Banco de Alta se quedó estancado en 2800 PSI y no sube. No hay fugas audibles.""")
ans_47 = st.text_area("¿Es este un comportamiento normal? Describa la causa probable y qué componente específico revisaría:")

if st.button("Finalizar y Generar Reporte PDF"):
    if not nombre:
        st.error("Por favor, ingrese el nombre del técnico antes de finalizar.")
    else:
        # Calcular calificación
        aciertos = sum(1 for q in preguntas_db if q['id'] in respuestas_usuario and respuestas_usuario[q['id']] == q['c'])
        total_preguntas = len(preguntas_db)
        porcentaje = (aciertos / total_preguntas) * 100
        
        status = "REPROBADO"
        if porcentaje >= 85: status = "EXCELENTE / APROBADO"
        elif porcentaje >= 70: status = "APROBADO"

        # Generar archivo PDF
        pdf_file = generar_pdf(nombre, supervisor, fecha_eval, aciertos, total_preguntas, porcentaje, status, ans_46, ans_47)
        
        st.success(f"Evaluación concluida. Puntaje: {porcentaje:.1f}%")
        st.download_button(label="⬇️ Descargar Reporte Oficial (PDF)", 
                           data=pdf_file, 
                           file_name=f"Evaluacion_{nombre}.pdf", 
                           mime="application/pdf")
