import streamlit as st
import datetime
from PIL import Image

# Sayfa Yapılandırması - 'centered' ile içeriği dikey bir sütuna hapsediyoruz.
st.set_page_config(page_title="Saha Satış Denetimi", page_icon="🥃", layout="centered")

# --- ŞIK TASARIM İÇİN CUSTOM CSS ---
st.markdown("""
    <style>
    /* Ana Başlık Stili */
    .main-title {
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        color: #1E1E1E;
        margin-bottom: 20px;
    }
    
    /* Kanal Butonları Stili */
    div.stButton > button {
        height: 3.5em;
        font-size: 18px !important;
        font-weight: bold;
        border-radius: 12px;
        border: 1px solid #E0E0E0;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
    }
    
    div.stButton > button:hover {
        border-color: #FF4B4B;
        color: #FF4B4B;
        transform: translateY(-2px);
    }

    /* Checkbox (Ürünler) Alanı */
    .stCheckbox label {
        font-size: 20px !important;
        font-weight: 500;
        padding: 12px 5px;
        border-bottom: 1px solid #F0F2F6;
    }

    /* Kategori Başlıkları */
    .category-header {
        background-color: #F8F9FA;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 20px;
        border-left: 5px solid #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ YAPISI ---
category_data = {
    "Viski": ["J. Walker Black 70cl", "Chivas 12 YO 70cl", "Jack Daniel's 70cl", "Ballantine's 70cl"],
    "Rakı": ["Yeni Rakı 70cl", "Tekirdağ Altın 70cl", "Efe Yaş Üzüm 70cl", "Beylerbeyi Göbek 70cl"]
}
channels = {
    "Migros": ["Ataşehir MMM", "Caddebostan Jet", "Beşiktaş 5M", "Mecidiyeköy MMM"],
    "CarrefourSA": ["İstinye Hiper", "Kozyatağı Gurme", "Acıbadem Süper"],
    "Metro": ["Güneşli Toptancı", "Kozyatağı Toptancı"]
}

# --- UYGULAMA BAŞLANGICI ---
st.markdown('<div class="main-title">🛡️ B2B SAHA DENETİMİ</div>', unsafe_allow_html=True)

# 1. KANAL SEÇİMİ (YANYANA ŞIK BUTONLAR)
if 'selected_channel' not in st.session_state:
    st.session_state.selected_channel = None

st.write("### 1. Kanal Seçiniz")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🍊 Migros", use_container_width=True):
        st.session_state.selected_channel = "Migros"
with c2:
    if st.button("🔵 Carrefour", use_container_width=True):
        st.session_state.selected_channel = "CarrefourSA"
with c3:
    if st.button("⚪ Metro", use_container_width=True):
        st.session_state.selected_channel = "Metro"

# Kanal seçildikten sonra geri kalan kısım açılır
if st.session_state.selected_channel:
    ch = st.session_state.selected_channel
    st.divider()

    # 2. MAĞAZA SEÇİMİ (ARAMA BARLI)
    st.write(f"### 2. {ch} Mağaza Arama")
    store_choice = st.selectbox(
        "Mağaza ismini yazın:",
        options=channels[ch],
        index=None,
        placeholder="Mağaza adı giriniz..."
    )

    if store_choice:
        st.divider()
        
        # 3. ÜRÜN LİSTESİ
        st.write("### 3. Ürün Kontrolü")
        st.info("Eksik ürünlerin işaretini kaldırın.")
        
        check_results = {}
        
        st.markdown('<div class="category-header">🥃 VİSKİ GRUBU</div>', unsafe_allow_html=True)
        for p in category_data["Viski"]:
            check_results[p] = st.checkbox(p, value=True, key=f"v_{p}")
            
        st.markdown('<div class="category-header">🍶 RAKI GRUBU</div>', unsafe_allow_html=True)
        for p in category_data["Rakı"]:
            check_results[p] = st.checkbox(p, value=True, key=f"r_{p}")

        st.divider()

        # 4. FOTOĞRAF
        st.write("### 4. Reyon Fotoğrafı")
        uploaded_file = st.file_uploader("📷 Fotoğraf Çek veya Yükle", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            st.image(Image.open(uploaded_file), use_container_width=True)

        st.divider()

        # 5. GÖNDER BUTONU
        if st.button("✅ DENETİMİ TAMAMLA", use_container_width=True, type="primary"):
            st.balloons()
            st.success(f"{store_choice} denetimi başarıyla sisteme iletildi!")
            
            # Resetleme butonu (İsteğe bağlı)
            if st.button("Yeni Kayıt"):
                st.session_state.selected_channel = None
                st.rerun()

else:
    st.info("Lütfen bir kanal seçerek başlayın.")