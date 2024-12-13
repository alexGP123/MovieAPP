import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

# Cargar las credenciales desde st.secrets
key_dict = st.secrets["firebase"]  # No necesitas json.loads aquí
creds = service_account.Credentials.from_service_account_info(key_dict)

# Conectar a Firestore
db = firestore.Client(credentials=creds, project=key_dict["project_id"])

# Cargar datos desde Firestore
names_ref = list(db.collection(u'names').stream())
names_dict = list(map(lambda x: x.to_dict(), names_ref))
df = pd.DataFrame(names_dict)

# Configuración de la página
st.set_page_config(page_title="Netflix App", layout="wide")

# Título principal
st.title("Netflix app")
st.write("Done! (using st.cache)")

# Sidebar
st.sidebar.header("Opciones de búsqueda")

# Checkbox para mostrar todos los filmes
mostrar_todos = st.sidebar.checkbox("Mostrar todos los filmes", value=True)

# Campo de texto para buscar por título
titulo_filme = st.sidebar.text_input("Título del filme:", "")

# Botón para buscar filmes
if st.sidebar.button("Buscar filmes"):
    if titulo_filme:
        df = df[df['name'].str.contains(titulo_filme, case=False, na=False)]

# Dropdown para filtrar por director
directores = df['director'].dropna().unique()
director_seleccionado = st.sidebar.selectbox("Seleccionar Director", ["Todos"] + list(directores))

if st.sidebar.button("Filtrar director"):
    if director_seleccionado != "Todos":
        df = df[df['director'] == director_seleccionado]

# Formulario para agregar un nuevo filme
st.sidebar.subheader("Nuevo filme")
with st.sidebar.form("nuevo_filme"):
    # Campo de texto para el nombre del filme
    nuevo_nombre = st.text_input("Name:")

    # Menú desplegable para seleccionar la compañía
    companias = ["Warner Bros.", "Universal Pictures", "Paramount Pictures", "Sony Pictures"]
    nueva_compania = st.selectbox("Company", companias)

    # Menú desplegable para seleccionar el director
    directores = ["Danny Huston", "Christopher Nolan", "Steven Spielberg", "Quentin Tarantino"]
    nuevo_director = st.selectbox("Director", directores)

    # Menú desplegable para seleccionar el género
    generos = ["Drama", "Comedy", "Action", "Horror", "Sci-Fi"]
    nuevo_genero = st.selectbox("Genre", generos)

    # Botón para enviar el formulario
    enviado = st.form_submit_button("Crear nuevo filme")

    if enviado:
        if nuevo_nombre and nueva_compania and nuevo_director and nuevo_genero:
            nuevo_filme = {
                "name": nuevo_nombre,
                "company": nueva_compania,
                "director": nuevo_director,
                "genre": nuevo_genero
            }
            db.collection(u'names').add(nuevo_filme)
            st.success("¡Nuevo filme agregado!")
        else:
            st.error("Por favor, completa todos los campos.")

# Mostrar tabla de filmes
st.subheader("Todos los filmes")
st.dataframe(df)