
import streamlit as st
import joblib

# Cargar modelo y vectorizador
modelo = joblib.load("modelo.pkl")
vectorizador = joblib.load("vectorizador.pkl")

# Historial de chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Botón para limpiar chat
if st.button("🧹 Limpiar historial del chat"):
    st.session_state.chat = []

st.title("Clasificador de mensajes Chat Videojuegos")

mensaje = st.text_input("Escribe tu mensaje:")

if st.button("Enviar") and mensaje:
    X = vectorizador.transform([mensaje])
    categoria = modelo.predict(X)[0]

    if categoria in ["chitchat", "coordination"]:
        texto = f"{mensaje} ({categoria})"
        st.session_state.chat.append(("usuario", texto, "normal", categoria))
    elif categoria == "toxic":
        advertencia = f"⚠️ Este mensaje puede ser ofensivo ({categoria}): {mensaje}"
        st.session_state.chat.append(("usuario", advertencia, "toxic", categoria))
    elif categoria in ["racism", "religious", "sexist"]:
        razon = {
            "racism": "por lenguaje racista",
            "religious": "por lenguaje religioso ofensivo",
            "sexist": "por lenguaje sexista"
        }.get(categoria, "por lenguaje inaceptable")
        texto_ban = f"🚫 Has sido baneado del chat {razon}. (Clasificación: {categoria})"
        st.session_state.chat.append(("sistema", texto_ban, "banned", categoria))
    else:
        # Cualquier otra categoría desconocida se banea igualmente
        texto_ban = f"🚫 Has sido baneado del chat por lenguaje inaceptable. (Clasificación: {categoria})"
        st.session_state.chat.append(("sistema", texto_ban, "banned", categoria))

# Mostrar historial de mensajes
for autor, texto, tipo, categoria in st.session_state.chat:
    if tipo == "normal":
        st.markdown(f"**{autor}**: {texto}")
    elif tipo == "toxic":
        st.markdown(f"<div style='color:gray;'><strong>{autor}</strong>: {texto}</div>", unsafe_allow_html=True)
    elif tipo == "banned":
        st.markdown(f"<div style='color:red;'><strong>{autor}</strong>: {texto}</div>", unsafe_allow_html=True)
