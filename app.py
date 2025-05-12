# app.py

import streamlit as st
import os
from openai import OpenAI

# Configurar clave API
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Configurar diseño
st.set_page_config(page_title="LexDomus MVP", layout="centered")

# Título
st.title("⚖️ LexDomus – Asistente Jurídico Deliberativo")
st.markdown("Una aplicación basada en IA explicativa para analizar cláusulas contractuales en propiedad intelectual.")

st.markdown("---")

# Módulo 1: Entrada de cláusula
st.header("🔍 1. Introducción de la cláusula")
st.caption("Introduce una cláusula contractual real para su análisis.")
st.info("💡 Esta cláusula será el punto de partida para el razonamiento jurídico automatizado.")
clausula_usuario = st.text_area(
    "Cláusula contractual",
    height=200,
    placeholder="Ejemplo: El autor cede todos los derechos sobre la obra en todo el mundo, sin límite temporal..."
)

# Módulo 2: Selección de jurisdicción
st.header("🌍 2. Jurisdicción aplicable")
st.caption("Selecciona el marco legal en el que debe analizarse la cláusula.")
jurisdiccion = st.selectbox(
    "Jurisdicción principal",
    options=["España", "EE.UU.", "Ambas"]
)

# Módulo 3: Contexto legal (RAG simulado)
st.header("📚 3. Normativa aplicada (RAG simulado)")
st.caption("Estos son los textos legales que la IA utilizará como base para el análisis. Esto garantiza trazabilidad y evita 'alucinaciones'.")
contexto_legal = """
1. España – Art. 17 LPI:
“Corresponde al autor el ejercicio exclusivo de los derechos de explotación de su obra sin más limitaciones que las establecidas por la ley.”

2. EE.UU. – 17 U.S.C. §106:
“El titular del copyright tiene el derecho exclusivo de reproducir, preparar obras derivadas, distribuir copias y comunicar la obra públicamente.”

3. Convenio de Berna – Art. 6bis:
“El autor conservará el derecho de reivindicar la paternidad de la obra y de oponerse a toda deformación o modificación de la misma.”
"""
st.code(contexto_legal, language="markdown")

# Botón para lanzar análisis
st.markdown("---")
st.header("🚀 4. Iniciar análisis deliberativo")
st.caption("El sistema analizará la cláusula, propondrá mejoras y evaluará el equilibrio del razonamiento.")
analizar = st.button("Analizar cláusula con GPT-4")

# Proceso de análisis
if analizar:

    prompt = f"""
Actúa como un asistente jurídico deliberativo experto en propiedad intelectual internacional.

Tu tarea es analizar la siguiente cláusula legal desde una perspectiva comparativa, utilizando únicamente los textos legales proporcionados más abajo.

Descompón el análisis en estos pasos:
1. Subpreguntas jurídicas clave.
2. Validez de la cláusula en {jurisdiccion}.
3. Propuesta de cláusula alternativa, si fuera necesario.
4. Evaluación del equilibrio epistémico (pluralidad, trazabilidad y justificación).

{contexto_legal}

Cláusula a analizar:
\"\"\"
{clausula_usuario}
\"\"\"
"""

    with st.spinner("⌛ Analizando la cláusula..."):

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )

            resultado = response.choices[0].message.content

            # Mostrar resultado paso a paso
            st.success("✅ Análisis completo generado.")
            st.markdown("---")
            st.header("🧠 5. Resultado del análisis jurídico")

            # Subbloques extraídos por cabeceras
            bloques = resultado.split("###")

            for bloque in bloques:
                if "Subpreguntas" in bloque:
                    with st.expander("🧩 Subpreguntas jurídicas"):
                        st.caption("La IA identifica las preguntas clave necesarias para evaluar jurídicamente la cláusula.")
                        st.markdown(bloque)
                elif "Validez" in bloque:
                    with st.expander("📐 Validez jurídica según jurisdicción"):
                        st.caption("Comparación legal según la legislación seleccionada.")
                        st.markdown(bloque)
                elif "alternativa" in bloque or "sugerida" in bloque:
                    with st.expander("✍️ Cláusula alternativa sugerida"):
                        st.caption("Una propuesta de redacción más clara y jurídicamente sólida.")
                        st.markdown(bloque)
                elif "equilibrio" in bloque.lower():
                    with st.expander("⚖️ Evaluación epistémica del razonamiento"):
                        st.caption("Se valora la pluralidad, trazabilidad y justificación del análisis.")
                        st.markdown(bloque)
                else:
                    with st.expander("📄 Otros contenidos"):
                        st.markdown(bloque)

        except Exception as e:
            st.error(f"❌ Error al contactar con OpenAI: {str(e)}")
