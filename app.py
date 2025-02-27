import streamlit as st
from openai import OpenAI

#Configurar openai
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

#Tiutlo de pagina
st.title("OpenAI GPT-4o")

#variable de sesion de historia de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

#Historia de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#chat input
if prompt := st.chat_input("escribe tu mensaje aqui..."):
    with st.chat_message("user"):
        st.markdown(prompt)

#añadir el mensaje de usuario a la hitoria de chat
st.session_state.messages.append({"role": "user", "content": prompt})

#Obtener respuesta de OpenAI
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    try:
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                 "content": "Eres un asistente de atención al cliente y solo puedes responder sobre <horarios>, <productos> (solo sobre <telefonos>, <laptops> e <impresoras>) y <devoluciones>. Si te preguntan sobre otros temas, responde educadamente que no puedes proporcionar esa información. Responde de manera clara y profesional. Ejemplos: - Horarios: Responde con los horarios de apertura y cierre. Ejemplo: ¿Cuáles son los horarios de atención? Respuesta: Lunes a viernes, 9:00 a 18:00 horas. - Productos: Responde sobre disponibilidad, características o precios de <telefonos>, <laptops> o <impresoras>. Ejemplo: ¿Tienen el producto XYZ en stock? Respuesta: Sí, está disponible en la sección de [categoría]. - Devoluciones: Explica la política de devoluciones y requisitos. Ejemplo: ¿Cómo puedo hacer una devolución? Respuesta: Debes traer el producto con el recibo dentro de los 30 días posteriores. Si la pregunta es fuera de estas categorías, responde: Lo siento, solo puedo ofrecerte información sobre horarios, productos y devoluciones."},
                 *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ],
            stream = True
        )
        
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                message_placeholder.markdown(full_response + "...")

        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        


    except Exception as e:
     st.error(f"Error: {str(e)}")
     