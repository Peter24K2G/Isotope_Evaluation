import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import folium
import geopandas as gpd
from streamlit_folium import folium_static

st.sidebar.title("Resultados Hidrogeológicos EL EDEN")

# Cargar datos
df = pd.read_excel("./data.xlsx")
df = df.loc[df["Autor"]=="UNAL"]

# Definir las líneas de referencia para el gráfico isotópico
delta18O = np.linspace(-9, -7.85, num=50)
delta2H = delta18O * 8.03 + 9.66
Sadelta18O = np.linspace(-9, -7.85, num=50)
Sadelta2H = Sadelta18O * 8.02 + 12.12  # Saylor

# Título de la sección
st.markdown("# Resultados Isótopos Estables")

# Selección de agrupación por color y símbolo
# col1, col2 = st.columns(2)
# with col1:
#     color = st.selectbox(
#         "Seleccione agrupación por color",
#         df.columns,
#     )

# with col2:
#     symbol = st.selectbox(
#         "Seleccione agrupación por símbolo",
#         df.columns
#     )

# Crear el gráfico isotópico interactivo
fig = px.scatter(df, y="2H", x="O18", symbol="tipo", color="Nombre")
fig.update_traces(textposition='top center', textfont=dict(size=11))
fig.update_layout(
   yaxis_title='d2H',
   xaxis_title='d18O',
   showlegend=True
)
fig.add_trace(go.Scatter(y=delta2H, x=delta18O, mode='lines', name='CML - (Rodriguez, 2004)', line=dict(color='darkgray')))
fig.add_trace(go.Scatter(y=Sadelta2H, x=Sadelta18O, mode='lines', name='CML - (Saylor et al., 2009)', line=dict(color='gray')))

# Mostrar el gráfico isotópico
st.plotly_chart(fig)


col1, col2, col3 = st.columns(3)

with col1:
    # Crear un widget multiselect para que el usuario seleccione los puntos de interés
    selected_points1 = st.multiselect(
        "Seleccione puntos para el grupo 1",
        options=df.index,
        format_func=lambda x: f"{df.loc[x,"Autor"]}:{df.loc[x, 'Nombre']}"
        # format_func=lambda x: f"O18: {df.loc[x, 'O18']}, 2H: {df.loc[x, '2H']}"
    )

with col2:
        # Crear un widget multiselect para que el usuario seleccione los puntos de interés
    selected_points2 = st.multiselect(
        "Seleccione puntos para el grupo 2",
        options=df.index,
        format_func=lambda x: f"{df.loc[x,"Autor"]}:{df.loc[x, 'Nombre']}"
        # format_func=lambda x: f"O18: {df.loc[x, 'O18']}, 2H: {df.loc[x, '2H']}"
    )

with col3:
        # Crear un widget multiselect para que el usuario seleccione los puntos de interés
    selected_points3 = st.multiselect(
        "Seleccione puntos para el grupo 3",
        options=df.index,
        format_func=lambda x: f"{df.loc[x,"Autor"]}:{df.loc[x, 'Nombre']}"
        # format_func=lambda x: f"O18: {df.loc[x, 'O18']}, 2H: {df.loc[x, '2H']}"
    )

# Filtrar el DataFrame según los puntos seleccionados
if selected_points1:
    df_selected1 = df.loc[selected_points1]
    df_selected1["Grupo"] = '1'
else:
    df_selected1 = df

    # Filtrar el DataFrame según los puntos seleccionados
if selected_points2:
    df_selected2 = df.loc[selected_points2]
    df_selected2["Grupo"] = '2'
else:
    df_selected2 = df

if selected_points3:
    df_selected3 = df.loc[selected_points3]
    df_selected3["Grupo"] = '3'
else:
    df_selected3 = df


df_selected = pd.concat([df_selected1,df_selected2,df_selected3])

def icon_by_water_type(tipo):
    if tipo == 'Subterranea':
        return folium.Icon(color='blue', icon='tint')  # Gota de agua para agua subterránea
    elif tipo == 'Infiltracion':
        return folium.Icon(color='green', icon='arrow-down')  # Flecha hacia abajo para infiltraciones
    elif tipo == 'Superficial':
        return folium.Icon(color='lightblue', icon='cloud')  # Nube para agua superficial
    else:
        return folium.Icon(color='gray', icon='question-sign')  # Icono genérico para otros tipos
    
def color_by_group(color):
    if color == "1":
        return "#0068c9"
    elif color == "2":
        return "#83c9ff"
    elif color == "3":
        return "#ff2b2b"
    else:
        return "black"

# Crear el mapa Folium con los puntos seleccionados
st.markdown("## Mapa de Ubicaciones")

# Inicializar el mapa en una localización central
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=14)

# Agregar marcadores solo para los puntos seleccionados
for i, row in df_selected.iterrows():
    tipo_muestra = row["tipo"]
    color = color_by_group(row["Grupo"])
    st.write(tipo_muestra)
    folium.Marker([row['lat'], row['lon']], popup=f"{row["Autor"]}:{row["Nombre"]}",
                tooltip = folium.Tooltip(f'<span style="color: {color};">{row["Autor"]}:{row["Nombre"]}</span>', permanent=True),
                icon=icon_by_water_type(tipo_muestra)
                ).add_to(m)
    

shapefile_path = "mygeodata\KMZ_TUNEL\Line_Features-line.shp"
gdf = gpd.read_file(shapefile_path)

# Convertir a GeoJSON
geojson_data = gdf.to_json()

folium.GeoJson(geojson_data).add_to(m)

# Mostrar el mapa en Streamlit
folium_static(m)


nfig = px.scatter(df_selected, y="2H", x="O18", symbol="Nombre", color="Grupo")
nfig.add_trace(go.Scatter(y=delta2H, x=delta18O, mode='lines', name='CML - (Rodriguez, 2004)', line=dict(color='darkgray')))
nfig.add_trace(go.Scatter(y=Sadelta2H, x=Sadelta18O, mode='lines', name='CML - (Saylor et al., 2009)', line=dict(color='gray')))
st.plotly_chart(nfig)

# st.write(df_selected)