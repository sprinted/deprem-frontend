import os
import requests
import streamlit as st

import folium
import streamlit_folium as st_folium

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

api_endpoint = os.getenv("API_ENDPOINT")


def sidebar():
    # Displaying sidebar
    st.sidebar.title("Deprem Project")
    st.sidebar.markdown(
        """
    Deprem bölgesinin verilerini görselleştirmeyi amaçlayan bir projedir.
    """
    )

    sidebar_options = requests.get(f"{api_endpoint}/select_options").json()
    with st.sidebar.form("user-form"):
        current_user_input = {}
        final_user_input = {}
        coordinates_data = {}

        for i in sidebar_options:
            current_sidebar_values = sidebar_options[i]
            if "" not in current_sidebar_values:
                current_sidebar_values.insert(0, "")

            if "_" in i:
                j = i.replace("_", " ").replace("konum","").capitalize()
            else:
                j = i.capitalize()

            current_user_input[i] = st.selectbox(
                j, current_sidebar_values, index=current_sidebar_values.index("")
            )

        submitted = st.form_submit_button("Ara")
        if submitted:
            # Remove the "" values from the user input
            for z in current_user_input:
                if current_user_input[z] != "":
                    final_user_input[z] = current_user_input[z]

            st.success("Your options are displayed on the map 📍")

            coordinates_data = requests.get(
                f"{api_endpoint}/get_user_parameters", json=final_user_input
            ).json()

    draw_map(coordinates_data)


def draw_map(coordinates_data: dict):
    if coordinates_data:
        m = folium.Map(location=[37.7981263, 36.1829598], zoom_start=6)
        with st.expander("Show Data"):
            for x in coordinates_data:
                try:
                    if (
                            x["lat"]
                            and x["lon"]
                            and x["lat"] != ""
                            and x["lon"] != ""
                    ):
                        if x['lat'] and x['lon'] and x['lat'] != '' and x['lon'] != '':
                            location = f"http://maps.google.com/?ll={x['lat']},{x['lon']}"
                        else:
                            location = "Konum Bilgisi Yok"
                        folium.Marker(
                            location=[x["lat"], x["lon"]],
                            popup=f"""
                            İl: {x['konum_il']} |
                            İlçe: {x['konum_ilce']} |
                            Mahalle: {x['konum_mahalle']} <br>
                            İsim Soyisim: {x['isimsoyisim']} |
                            Kişi Sayısı: {x['kisi_sayisi']} |
                            Telefon Numrası: {x['telefon']} <br>
                            Adres: {x['adres']} |
                            Apartman: {x['apartman']} |
                            Sokak: {x['sokak']} |
                            Blok: {x['blok_no']} |
                            Kat: {x['kat']} <br>
                            Google Maps Linki: {location}
                            """,
                            tooltip=f"{x['konum_ilce']}",
                        ).add_to(m)

                        
                except KeyError:
                    pass
        

        st_folium.folium_static(m, width=1400, height=600)



st.set_page_config(layout="wide")
sidebar()
