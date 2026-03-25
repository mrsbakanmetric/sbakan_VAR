import streamlit as st
import datetime
from PIL import Image

# Sayfa Yapılandırması
st.set_page_config(page_title="Alkol Kategori Denetimi", page_icon="🥃", layout="wide")

# --- VERİ YAPISI ---
category_data = {
    "Viski": ["Johnnie Walker Black Label 70cl", "Chivas Regal 12 YO 70cl", "Jack Daniel's Old No.7 70cl", "Ballantine's Finest 70cl", "Jameson Irish Whiskey 70cl"],
    "Rakı": ["Yeni Rakı 70cl", "Tekirdağ Altın Seri 70cl", "Yeni Rakı Giz 50cl", "Efe Yaş Üzüm 70cl", "Beylerbeyi Göbek 70cl"]
}

channels = {
    "Migros": ["Ataşehir MMM", "Caddebostan Jet", "Beşiktaş 5M", "Mecidiyeköy MMM", "Bahçeşehir 5M", "Suadiye Jet"],
    "CarrefourSA": ["İstinye Hiper", "Kozyatağı Gurme", "Acıbadem Süper", "Fulya Hiper", "Maltepe Park Hiper"],
    "Metro": ["Güneşli Toptancı", "Kozyatağı Toptancı", "Pendik Toptancı", "Ayazağa Toptancı"]
}

# --- SESSION STATE ---
if 'selected_channel' not in st.session_state:
    st.session_state['selected_channel'] = None

st.title("🥃 B2B Saha Satış: Viski & Rakı Denetimi")
st.write(f"Sorumlu: **Ahmet Yılmaz** | Tarih: {datetime.date.today().strftime('%d/%m/%Y')}")
st.divider()

# --- 1. KANAL SEÇİMİ (BUTONLAR) ---
st.header("1. Kanal Seçiniz")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🍊 Migros", use_container_width=True):
        st.session_state['selected_channel'] = "Migros"
with col2:
    if st.button("🔵 CarrefourSA", use_container_width=True):
        st.session_state['selected_channel'] = "CarrefourSA"
with col3:
    if st.button("⚪ Metro", use_container_width=True):
        st.session_state['selected_channel'] = "Metro"

# --- 2. MAĞAZA ARAMA VE SEÇİMİ ---
if st.session_state['selected_channel']:
    current_channel = st.session_state['selected_channel']
    st.divider()
    
    st.header(f"2. {current_channel} Mağaza Arama & Seçim")
    
    # İPUCU: selectbox zaten arama özelliğine sahiptir.
    # Ancak kullanıcıya "Yazarak arayabilirsiniz" mesajı vermek deneyimi iyileştirir.
    store_list = channels[current_channel]
    
    store_choice = st.selectbox(
        "Mağaza adını yazın veya listeden seçin:",
        options=store_list,
        index=None, # Varsayılan olarak boş başlasın
        placeholder="Örn: Ataşehir veya Toptancı...",
        help="Yazmaya başladığınızda sonuçlar filtrelenir."
    )
    
    if store_choice:
        st.success(f"Seçili Mağaza: **{store_choice}**")
        st.divider()

        # --- 3. ÜRÜN KONTROLLERİ ---
        st.header("3. Assortment Check")
        check_results = {}

        tab1, tab2 = st.tabs(["🥃 VİSKİ", "🍶 RAKİ"])
        
        with tab1:
            for product in category_data["Viski"]:
                check_results[product] = st.checkbox(product, value=True, key=f"v_{product}")
        
        with tab2:
            for product in category_data["Rakı"]:
                check_results[product] = st.checkbox(product, value=True, key=f"r_{product}")

        st.divider()

        # --- 4. FOTOĞRAF ---
        st.header("4. Reyon Görseli")
        uploaded_file = st.file_uploader("Kamerayı aç veya dosya seç", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            st.image(Image.open(uploaded_file), use_container_width=True)

        st.divider()
        
        # --- GÖNDERME ---
        if st.button("✅ DENETİMİ TAMAMLA", use_container_width=True, type="primary"):
            st.balloons()
            st.success(f"{store_choice} denetimi başarıyla sisteme iletildi.")
            # Burada verileri kaydetme kodu (Google Sheets vb.) çalışacak.
