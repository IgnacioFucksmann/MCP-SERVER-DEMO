import re
import streamlit as st
from server import (
    agregar_usuario_mcp,
    eliminar_usuario_mcp,
    modificar_usuario_mcp,
    consultar_usuario_mcp,
)
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Demo Chat MCP")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Escribe tu mensaje:")


def extraer_datos_usuario(texto):
    # Elimina signos de puntuación que puedan molestar
    texto = texto.replace(":", " ").replace(",", " ")
    # Busca el email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", texto)
    if not email_match:
        return None
    email = email_match.group(0)
    # Busca la contraseña después de palabras clave o después del email
    pass_match = re.search(r"(?:contraseña|password|clave)?\s*([^\s]+)$", texto)
    if not pass_match:
        return None
    password = pass_match.group(1)
    # Busca el nombre entre la palabra clave y el email
    nombre_match = re.search(
        r"(?:usuario|alta|agrega|registrar|insertar)\s+a?\s*([\w\s]+?)\s+(?:con\s+el\s+email|email|correo|mail)?",
        texto,
        re.IGNORECASE,
    )
    if not nombre_match:
        return None
    nombre = nombre_match.group(1).strip()
    return nombre, email, password


client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # cualquier string, no se valida
)


def responder_llm(mensaje_usuario):
    respuesta = client.chat.completions.create(
        model="llama3", messages=[{"role": "user", "content": mensaje_usuario}]
    )
    return respuesta.choices[0].message.content


def detectar_accion(texto):
    texto = texto.lower()
    if any(pal in texto for pal in ["eliminar", "borrar", "quitar"]):
        return "eliminar"
    elif any(pal in texto for pal in ["modificar", "cambiar", "actualizar"]):
        return "modificar"
    elif any(
        pal in texto for pal in ["consultar", "mostrar", "buscar", "ver", "listar"]
    ):
        return "consultar"
    elif any(pal in texto for pal in ["agregar", "alta", "insertar", "registrar"]):
        return "agregar"
    else:
        return None


if st.button("Enviar") and user_input:
    st.session_state.messages.append(("user", user_input))
    accion = detectar_accion(user_input)
    if accion == "agregar":
        datos = extraer_datos_usuario(user_input)
        if datos:
            nombre, email, password = datos
            respuesta = agregar_usuario_mcp(nombre, email, password)
        else:
            respuesta = "No entendí los datos para agregar el usuario."
    elif accion == "eliminar":
        email_match = re.search(r"[\w\.-]+@[\w\.-]+", user_input)
        if email_match:
            respuesta = eliminar_usuario_mcp(email_match.group(0))
        else:
            respuesta = "Por favor, indica el email del usuario a eliminar."
    elif accion == "modificar":
        email_match = re.search(r"[\w\.-]+@[\w\.-]+", user_input)
        nombre_match = re.search(r"nombre\\s*=\\s*([\\w\\s]+)", user_input)
        pass_match = re.search(
            r"(?:contraseña|password|clave)\\s*=\\s*([^\\s]+)", user_input
        )
        email = email_match.group(0) if email_match else None
        nuevo_nombre = nombre_match.group(1).strip() if nombre_match else None
        nuevo_password = pass_match.group(1) if pass_match else None
        if email and (nuevo_nombre or nuevo_password):
            respuesta = modificar_usuario_mcp(email, nuevo_nombre, nuevo_password)
        else:
            respuesta = "Por favor, indica el email y el nuevo nombre y/o contraseña."
    elif accion == "consultar":
        email_match = re.search(r"[\w\.-]+@[\w\.-]+", user_input)
        email = email_match.group(0) if email_match else None
        respuesta = consultar_usuario_mcp(email)
    else:
        respuesta = responder_llm(user_input)
    st.session_state.messages.append(("bot", respuesta))

for sender, msg in st.session_state.messages:
    st.write(f"**{sender}:** {msg}")
