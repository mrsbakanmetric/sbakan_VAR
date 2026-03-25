import streamlit as st
import datetime
from PIL import Image

# 1. Mobil Tasarım Ayarı (Layout 'centered' yaparak ekranın yayılmasını engelliyoruz)
st.set_page_config(page_title="Saha Denetim", page_icon="🥃", layout="centered")

# --- CSS: Butonları ve Checkboxları Büyütme ---
st.markdown("""
    <style>
    /* Buton metinlerini büyüt */
    div.stButton > button {
        height: 4em;
        font-size: 20px !important;
        font-weight: bold;
        border-radius: 10px;
    }
    /* Checkbox (Onay kutusu) metinlerini büyüt */
    .stCheckbox label {
        font-size: 22px !important;
        font-weight: 500;
        padding: 10px 0px;
    }
    /* Selectbox (Arama barı) yüksekliğini artır */
    .stSelectbox div[data-baseweb="select"] {
        height: 60px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ ---
category_data = {
    "Viski": ["J. Walker Black 70cl", "Chivas 12 YO 70cl", "Jack Daniel's 70cl", "Ballantine's 70cl"],
    "Rakı": ["Yeni Rakı 70cl", "Tekirdağ Altın 70cl", "Efe Yaş Üzüm 70cl", "Beylerbeyi Göbek 70cl"]
}
channels = {
    "Migros": ["Ataşehir MMM", "Caddebostan Jet", "Beşiktaş 5M"],
    "CarrefourSA": ["İstinye Hiper", "Kozyatağı Gurme", "Acıbadem Süper"],
    "Metro": ["Güneşli Toptancı", "Kozyatağı Toptancı"]
}

if 'step' not in st.session_state: st.session_state.step = 1
if 'channel' not in st.session_state: st.session_state.channel = None

# --- UYGULAMA AKIŞI ---

# ADIM 1: KANAL SEÇİMİ
if st.session_state.step == 1:
    st.subheader("📍 Kanal Seçiniz")
    for ch in channels.keys():
        if st.button(ch, use_container_width=True):
            st.session_state.channel = ch
            st.session_state.step = 2
            st.rerun()

# ADIM 2: MAĞAZA ARAMA VE SEÇİM
elif st.session_state.step == 2:
    st.subheader(f"🏬 {st.session_state.channel} Mağazası")
    
    store_choice = st.selectbox(
        "Mağaza Ara/Seç:",
        options=channels[st.session_state.channel],
        index=None,
        placeholder="Yazmaya başlayın..."
    )
    
    col1, col2 = st.columns(2)
    if col1.button("⬅️ Geri"):
        st.session_state.step = 1
        st.rerun()
    
    if store_choice:
        if col2.button("İlerle ➡️"):
            st.session_state.store = store_choice
            st.session_state.step = 3
            st.rerun()

# ADIM 3: ÜRÜN KONTROLÜ & FOTOĞRAF
elif st.session_state.step == 3:
    st.subheader(f"📋 {st.session_state.store}")
    
    st.write("### 🥃 VİSKİ")
    for p in category_data["Viski"]:
        st.checkbox(p, value=True, key=f"v_{p}")
        
    st.write("### 🍶 RAKI")
    for p in category_data["Rakı"]:
        st.checkbox(p, value=True, key=f"r_{p}")
    
    st.divider()
    
    st.write("### 📷 FOTOĞRAF")
    uploaded_file = st.file_uploader("Kamerayı Aç", type=['png', 'jpg', 'jpeg'])
    
    if st.button("✅ DENETİMİ BİTİR", use_container_width=True, type="primary"):
        st.balloons()
        st.success("Veriler iletildi!")
        if st.button("Yeni Denetim"):
            st.session_state.step = 1
            st.rerun()