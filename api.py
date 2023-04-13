import streamlit as st
import pandas as pd
import requests


with st.form("app", clear_on_submit=True):
    unidade = st.text_input("Conta Contrato",placeholder="Ex: 3000881235")
    btn = st.form_submit_button("VERIFICAR")
    url = f"https://api-al-cliente.equatorialenergia.com.br/api/v1/instalacao/{unidade}/"

    if btn:
        try:
            query = requests.get(url)
            response = query.json()
            if response["status"] is None:
                st.error("Unidade não cadastrada / Coordenadas não disponíveis")
            else:
                col1, col2 = st.columns(2)
                lat = response["dadosTecnicos"]["coordenadaGeografica"]["latitude"]
                long = response["dadosTecnicos"]["coordenadaGeografica"]["longitude"]
                col1.info(unidade)
                col2.info(query.status_code)
                col1.code(body = float(lat.replace("-","")) * -1)
                col2.code(body = float(long.replace("-","")) * -1)
            with st.expander("RESPONSE"):
                st.json(response)

        except Exception as e:
            st.exception(e)
