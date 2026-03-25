import streamlit as st
import pandas as pd
from PIL import Image
import time
import random

# Sayfa Yapılandırması
st.set_page_config(page_title="FMCG Availability & Assortment Bot", page_icon="🥃", layout="centered")

# --- ŞIK TASARIM (CSS) ---
st.markdown("""
    <style>
    .main-title { font-size: 30px; font-weight: bold; text-align: center; color: #1E1E1E; margin-bottom: 5px; }
    .sub-title { font-size: 16px; text-align: center; color: #666; margin-bottom: 25px; }
    
    div.stButton > button {
        height: 3.5em;
        font-size: 18px !important;
        font-weight: bold;
        border-radius: 12px;
        transition: 0.3s;
    }
    
    .score-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
        text-align: center;
        margin: 15px 0px;
    }
    .score-value { font-size: 45px; font-weight: bold; }
    .extra-header { color: #D9534F; font-weight: bold; margin-top: 20px; border-bottom: 2px solid #D9534F; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. SİDEBAR: DİNAMİK PORTFÖY YÖNETİMİ ---
with st.sidebar:
    st.subheader("⚙️ Portföy Yönetimi")
    st.caption("Beklenen SKU'ları düzenleyin. Analiz sırasında bu listede olmayanlar 'Ekstra' sayılacaktır.")
    
    if 'sku_list' not in st.session_state:
        st.session_state.sku_list = pd.DataFrame([
            {"Ürün Adı": "Yeni Rakı 70cl"},
            {"Ürün Adı": "Yeni Rakı 100cl"},
            {"Ürün Adı": "Tekirdağ Altın Seri"},
            {"Ürün Adı": "Beylerbeyi Göbek"}
        ])

    edited_sku = st.data_editor(
        st.session_state.sku_list,
        num_rows="dynamic",
        use_container_width=True,
        key="sku_editor"
    )
    st.session_state.sku_list = edited_sku

# --- 2. ANA EKRAN ---
st.markdown('<div class="main-title">🚀 FMCG Availability & Assortment Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI Destekli Saha Satış ve Denetim Sistemi</div>', unsafe_allow_html=True)

if 'selected_channel' not in st.session_state:
    st.session_state.selected_channel = None

st.write("### 1. Kanal Seçiniz")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🍊 Migros", use_container_width=True): st.session_state.selected_channel = "Migros"
with c2:
    if st.button("🔵 Carrefour", use_container_width=True): st.session_state.selected_channel = "Carrefour"
with c3:
    if st.button("⚪ Metro", use_container_width=True): st.session_state.selected_channel = "Metro"

stores_data = {
    "Migros": ["Ataşehir MMM", "Beşiktaş 5M", "Caddebostan Jet"],
    "Carrefour": ["İstinye Hiper", "Kozyatağı Gurme"],
    "Metro": ["Güneşli Toptancı", "Kozyatağı Toptancı"]
}

# --- 3. MAĞAZA VE ANALİZ AKIŞI ---
if st.session_state.selected_channel:
    ch = st.session_state.selected_channel
    st.divider()
    st.write(f"### 2. {ch} Mağaza Seçimi")
    store_choice = st.selectbox("Ma