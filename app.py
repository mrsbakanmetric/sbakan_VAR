import streamlit as st
import datetime
from PIL import Image

# Sayfa Yapılandırması
st.set_page_config(page_title="FMCG Saha Satış Botu", page_icon="🍺")

# Veri Yapısı
channels = {
    "Migros": {
        "stores": ["Ataşehir MMM", "Caddebostan Jet", "Beşiktaş 5M"],
        "assortment": ["Efes Pilsen 50cl", "Miller 33cl", "Budweiser 50cl"]
    },
    "CarrefourSA": {
        "stores": ["İstinye Hiper", "Kozyatağı Gurme", "Acıbadem Süper"],
        "assortment": ["Bomonti Filtresiz", "Carlsberg 33cl", "Corona 35.5cl"]
    },
    "Metro": {
        "stores": ["Güneşli Toptancı", "Kozyatağı Toptancı"],
        "assortment": ["Efes Özel Seri", "Amsterdam Navigator", "Weihenstephaner"]
    }
}

st.title("🛡️ FMCG B2B Saha Denetimi")

channel_choice = st.selectbox("Kanal Seçiniz:", ["Seçiniz"] + list(channels.keys()))

if channel_choice != "Seçiniz":
    store_choice = st.selectbox(f"{channel_choice} Mağaza Listesi:", channels[channel_choice]["stores"])
    
    st.header("Bulunabilirlik Kontrolü")
    check_results = {}
    for product in channels[channel_choice]["assortment"]:
        check_results[product] = st.checkbox(product, value=True)
    
    st.header("Raf Fotoğrafı")
    uploaded_file = st.file_uploader("Fotoğraf yükle", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_container_width=True)

    if st.button("Denetimi Tamamla"):
        st.success("Veriler başarıyla gönderildi!")
        st.json({"magaza": store_choice, "sonuc": check_results})


