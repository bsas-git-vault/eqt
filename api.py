import streamlit as st # pip install streamlit
import requests # Nativo

# INPUTS TEXT E BOTÃO
unidade = st.text_input("CC", placeholder="Ex: 3000881235")
btn = st.button("VERIFICAR")

# URL BASE COM O PARÂMETRO EM GET. RETORNA INFORMAÇÕES SOBRE A CC INFORMADA
URL_API = f"https://api-al-cliente.equatorialenergia.com.br/api/v1/instalacao/{unidade}/"

if btn:
        if not unidade.strip() or unidade.strip() is None:
             st.warning("Preencha o campo com o úmero da CC.")
             st.stop()
             st.empty()
        else:
            query = requests.get(URL_API)
            response = query.json()

            # COLETANDO LAT E LONG DO JSON
            lat = response["dadosTecnicos"]["coordenadaGeografica"]["latitude"]
            long = response["dadosTecnicos"]["coordenadaGeografica"]["longitude"]
            
            if lat and long:
                col1, col2 = st.columns(2)
                col1.info(unidade)
                col2.info(query.status_code)
                
                 # COMPONENTE EXPANDER COM JSON
                with st.expander("RESPONSE"):
                    st.json(response)

                # AJUSTANDO A STRING DAS COORDENADAS E TRANSFORMANDO EM FLOAT
                lat = float(lat.replace("-","")) * -1
                long = float(long.replace("-","")) * -1

                # USANDO O CAMPO CODE POR TER OPÇÃO DE COPIAR EMBUTIDA
                col1.code(body=lat)
                col2.code(body=long)

                # URL DE BUSCA DIRETO NO GOOGLE. O "2C" é o hex para "," NA TABELA ASCII. URLENCODING.
                URL_GOOGLE = f"https://www.google.com/search?q={lat}%2C{long}"
                
                # MARKDOWN QUE GERA LINK PARA GOOGLE
                st.markdown(f"Abrir no [Google]({URL_GOOGLE})")
            
            else:
                # DECLARANDO DUAS COLUNAS IDÊNTICAS
                st.error("Unidade não cadastrada / Coordenadas não disponíveis")