import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="netflix-adcac")

st.header("Aplicacion Netflix")
names_ref = list(db.collection(u'movies').stream())
names_dict = list(map(lambda x: x.to_dict(), names_ref))
names_dataframe = pd.DataFrame(names_dict)


################### filtrar data #################
st.sidebar.header("Buscar nombre de pelicula")
nameSearch = st.sidebar.text_input("nombre")
btnFiltrar = st.sidebar.button("Buscar")
if btnFiltrar:
  names_dataframe = names_dataframe[names_dataframe.name.str.contains(nameSearch,case=False)]

  if names_dataframe.shape[0] == 0:
    st.sidebar.write("Nombre no existe")

################## filtro por escritor ################

st.sidebar.header("Buscar nombre de director")
selected_director = st.sidebar.selectbox("Selecionar director", names_dataframe['director'].unique())
btnFiltrar2 = st.sidebar.button("Buscar director")

if btnFiltrar2:
  #names_dataframe = names_dataframe[(names_dataframe.director == selected_director) & (names_dataframe.name.str.contains(nameSearch,case=False))]
  names_dataframe = names_dataframe[(names_dataframe.director == selected_director) ]


################## nuevo registro ################

st.sidebar.header("Nuevo registro")
company = st.sidebar.text_input("Company")
director = st.sidebar.text_input("Director")
genre = st.sidebar.text_input("Genre")
name = st.sidebar.text_input("Name")
submit = st.sidebar.button("Crear nuevo registro")

# Once the name has submitted, upload it to the database
if company and director and genre and name and submit:
  doc_ref = db.collection("movies").document(name)
  doc_ref.set({
  "company": company,
  "director": director,
  "genre": genre,
  "name": name
  })
  st.sidebar.write("Registro insertado correctamente")
###################### fin ############################

st.text(str(names_dataframe.shape[0]) + ' peliculas encontradas')
st.dataframe(names_dataframe)




