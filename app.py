# app.py

import streamlit as st
import os
from openai import OpenAI

# Configurar clave API de OpenAI desde entorno seguro
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Configurar diseño de la app
st.set_page_config(page_title="LexDomus MVP", layout="centered")

# Título y descripción
st.title("LexDomus MVP – Asistente jurídico deliberativo")
st.markdown("""
Esta aplicación analiza cláusulas de cesión de derechos utilizando inteligencia artificial explicativa.  
Basada en GPT-4, simula razonamiento jurídico deliberativo fundado en normativa real.
""")

# Entrada de cláusula
st.subheader("1. Introduce una cláusula para analizar")
st.markdown("*¿Qué se introduce aquí? Pega una cláusula real de un contrato para analizar su validez jurídica.*")
clausula_usuario = st.text_area(
    label="Cláusula contractual:",
    height=200,
    placeholder="Ejemplo: El autor cede todos los derechos sobre la obra en todo el mundo, sin límite temporal..."
)

# Selección de jurisdicción
st.subheader("2. Selecciona la jurisdicción aplicable")
st.markdown("*¿Por qué elegir jurisdicción? La normativa aplicable afecta directamente a la validez de la cláusula.*")
jurisdiccion = st.selectbox(
    label="Jurisdicción principal",
    options=["España", "EE.UU.", "Ambas"]
)

# Botón para iniciar análisis
st.subheader("3. Iniciar análisis deliberativo")
st.markdown("*Al pulsar, se analizará la cláusula y se propondrá una versión mejorada si es necesario.*")
analizar = st.button("Analizar cláusula con GPT-4")

# Lógica de análisis
if analizar:

    contexto_legal = """
Contexto normativo para el análisis jurídico:

1. España – Art. 17 LPI:
“Corresponde al autor el ejercicio exclusivo de los derechos de explotación de su obra sin más limitaciones que las establecidas por la ley.”

2. EE.UU. – 17 U.S.C. §106:
“El titular del copyright tiene el derecho exclusivo de reproducir, preparar obras derivadas, distribuir copias y comunicar la obra públicamente.”

3. Convenio de Berna – Art. 6bis:
“El autor conservará el derecho de reivindicar la paternidad de la obra y de oponerse a toda deformación o modificación de la misma.”
"""

    prompt = f"""
Actúa como un asistente jurídico deliberativo experto en propiedad intelectual internacional.

Tu tarea es analizar la siguiente cláusula legal desde una perspectiva comparativa, utilizando únicamente los textos legales proporcionados más abajo.

Descompón el análisis en estos pasos:
1. Subpreguntas jurídicas clave.
2. Validez de la cláusula en {jurisdiccion}.
3. Propuesta de cláusula alternativa, si fuera necesario.
4. Evaluación del equilibrio epistémico (pluralidad, trazabilidad y justificación).

Sé claro, justifica cada paso con base normativa e indica cuándo una cláusula puede generar conflicto o nulidad.

{contexto_legal}

Cláusula a analizar:
\"\"\"
{clausula_usuario}
\"\"\"
"""

    # Enviar a GPT-4 y mostrar resultado
    with st.spinner("Analizando la cláusula con GPT-4..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            resultado = response.choices[0].message.content

            st.markdown("### Resultado del análisis jurídico:")
            st.markdown(resultado)

            # Enlaces de ayuda contextual
            st.markdown("---")
            st.markdown("**¿Qué significa cada parte del análisis?**")
            st.markdown("[Subpreguntas jurídicas](https://docs.google.com/...#subpreguntas)")
            st.markdown("[Comparación normativa](https://docs.google.com/...#comparacion)")
            st.markdown("[Validez legal](https://docs.google.com/...#validez)")
            st.markdown("[Cláusula alternativa](https://docs.google.com/...#clausulaalternativa)")
            st.markdown("[Evaluación epistémica (EEE)](https://docs.google.com/...#equilibrio)")

        except Exception as e:
            st.error(f"Ocurrió un error al contactar con OpenAI: {str(e)}")
