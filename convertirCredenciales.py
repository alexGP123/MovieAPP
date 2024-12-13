import toml
import json
import os

# Crear la carpeta .streamlit si no existe
if not os.path.exists(".streamlit"):
    os.makedirs(".streamlit")

# Cargar el archivo JSON
with open("firebase_credentials.json", "r") as json_file:
    firebase_credentials = json.load(json_file)

# Crear el archivo TOML
with open(".streamlit/secrets.toml", "w") as toml_file:
    toml.dump({"firebase": firebase_credentials}, toml_file)

print("Archivo secrets.toml creado exitosamente.")