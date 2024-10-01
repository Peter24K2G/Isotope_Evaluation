import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

st.sidebar.title("Resultados Hidrogeológicos EL EDEN")

# Cargar datos
df = pd.read_excel("./data.xlsx")

# Definir las líneas de referencia para el gráfico isotópico
delta18O = np.linspace(-10, -7.5, num=50)
delta2H = delta18O * 8.03 + 9.66
Sadelta18O = np.linspace(-10, -7.5, num=50)
Sadelta2H = Sadelta18O * 8.02 + 12.12  # Saylor

# Título de la sección
st.markdown("# Resultados Isótopos Estables")

# Selección de agrupación por color y símbolo
col1, col2 = st.columns(2)
with col1:
    color = st.selectbox(
        "Seleccione agrupación por color",
        df.columns,
    )

with col2:
    symbol = st.selectbox(
        "Seleccione agrupación por símbolo",
        df.columns
    )

# Crear el gráfico isotópico interactivo
fig = px.scatter(df, y="2H", x="O18", symbol=symbol, color=color)
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

# Crear un widget multiselect para que el usuario seleccione los puntos de interés
selected_points = st.multiselect(
    "Seleccione puntos para visualizar en el mapa",
    options=df.index,
    format_func=lambda x: f"{df.loc[x, 'Nombre']}"
    # format_func=lambda x: f"O18: {df.loc[x, 'O18']}, 2H: {df.loc[x, '2H']}"
)

# Filtrar el DataFrame según los puntos seleccionados
if selected_points:
    df_selected = df.loc[selected_points]
else:
    df_selected = df

# Crear el mapa Folium con los puntos seleccionados
st.markdown("## Mapa de Ubicaciones")

# Inicializar el mapa en una localización central
m = folium.Map(location=[df_selected['lat'].mean(), df_selected['lon'].mean()], zoom_start=14)

# Agregar marcadores solo para los puntos seleccionados
for i, row in df_selected.iterrows():
    folium.Marker([row['lat'], row['lon']], popup=f"{row["Nombre"]}").add_to(m)

# Mostrar el mapa en Streamlit
folium_static(m)


# Crear el gráfico isotópico interactivo
nfig = px.scatter(df_selected, y="2H", x="O18", symbol=symbol, color=color)
nfig.update_traces(textposition='top center', textfont=dict(size=11))
nfig.update_layout(
   yaxis_title='d2H',
   xaxis_title='d18O',
   showlegend=True
)
nfig.add_trace(go.Scatter(y=delta2H, x=delta18O, mode='lines', name='CML - (Rodriguez, 2004)', line=dict(color='darkgray')))
nfig.add_trace(go.Scatter(y=Sadelta2H, x=Sadelta18O, mode='lines', name='CML - (Saylor et al., 2009)', line=dict(color='gray')))
st.plotly_chart(nfig)