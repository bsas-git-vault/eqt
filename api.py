import streamlit as st
from streamlit_folium import st_folium
import requests
import folium

unidade = st.text_input("Conta Contrato",placeholder="Ex: 3000881235")
btn = st.button("VERIFICAR")
url = f"https://api-al-cliente.equatorialenergia.com.br/api/v1/instalacao/{unidade}/"

if btn:
    try:
        query = requests.get(url)
        response = query.json()
        if response["status"] is None:
            st.error("Unidade não cadastrada / Coordenadas não disponíveis")
        else:
            col1, col2 = st.columns(2)
            col1.info(unidade)
            col2.info(query.status_code)

            # COMPONENTE EXPANDER COM JSON
            with st.expander("JSON"):
                st.json(response)
            lat = response["dadosTecnicos"]["coordenadaGeografica"]["latitude"]
            long = response["dadosTecnicos"]["coordenadaGeografica"]["longitude"]

            # AJUSTANDO A STRING DAS COORDENADAS E TRANSFORMANDO EM FLOAT
            lat = float(lat.replace("-","")) * -1
            long = float(long.replace("-","")) * -1
            
            # DECLARA O MAPA COM LOCATION E ZOOM 
            map = folium.Map(location=[lat, long], zoom_start=15)

            #ADICIONANDO O MARCADOR NO PONTO
            folium.Marker(location=[lat, long], popup=unidade, tooltip=unidade).add_to(map)

            # RENDERIZANDO O MAPA
            try:
                map_render = st_folium(map, width=800)
            except Exception as ex:
                st.exception(ex)

            
            # with st.expander("MAPA"):

            # folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            #                  attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            #                 name="Esri.WorldImagery").add_to(map)
            # folium.LayerControl().add_to(map)
                
    except Exception as e:
        st.exception(e)
