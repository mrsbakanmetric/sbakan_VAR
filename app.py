import streamlit as st
import pandas as pd
from PIL import Image
import time

# Sayfa Yapılandırması
st.set_page_config(page_title="AI Saha Denetimi", page_icon="📸", layout="centered")

# --- CUSTOM CSS (Şık Tasarım) ---
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; text-align: center; color: #1E1E1E; }
    .stButton > button { height: 3.5em; border-radius: 12px; font-weight: bold; }
    .upload-box { border: 2px dashed #FF4B4B; padding: 20px; border-radius: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. SKU LİSTESİ YÜKLEME (ADMİN/YÖNETİCİ PANELİ) ---
st.sidebar.header("⚙️ Yönetici Paneli")
uploaded_sku_file = st.sidebar.file_uploader("SKU Listesini Yükle (Excel/CSV)", type=['xlsx', 'csv'])

# Varsayılan SKU Listesi (Dosya yüklenmezse kullanılacak)
if uploaded_sku_file is not None:
    if uploaded_sku_file.name.endswith('.csv'):
        sku_df = pd.read_csv(uploaded_sku_file)
    else:
        sku_df = pd.read_excel(uploaded_sku_file)
    st.sidebar.success("SKU Listesi Güncellendi!")
else:
    # Örnek Liste
    sku_df = pd.DataFrame({
        "Kategori": ["Viski", "Viski", "Rakı", "Rakı"],
        "Ürün Adı": ["Chivas Regal 12 YO", "JW Black Label", "Yeni Rakı 70cl", "Beylerbeyi Göbek"]
    })
    st.sidebar.info("Varsayılan SKU listesi aktif.")

# --- UYGULAMA ANA AKIŞ ---
st.markdown('<div class="main-title">📸 AI DESTEKLİ SAHA DENETİMİ</div>', unsafe_allow_html=True)

# Kanal Seçimi
if 'channel' not in st.session_state: st.session_state.channel = None

st.write("### 1. Kanal Seçiniz")
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("🍊 Migros", use_container_width=True): st.session_state.channel = "Migros"
with c2: 
    if st.button("🔵 Carrefour", use_container_width=True): st.session_state.channel = "Carrefour"
with c3: 
    if st.button("⚪ Metro", use_container_width=True): st.session_state.channel = "Metro"

if st.session_state.channel:
    st.divider()
    st.write(f"### 2. {st.session_state.channel} Mağaza Seçimi")
    store_choice = st.selectbox("Mağaza:", ["Ataşehir MMM", "Kozyatağı Hiper", "Güneşli Toptancı"], index=None, placeholder="Mağaza adı...")

    if store_choice:
        st.divider()
        st.write("### 3. AI Görüntü Analizi")
        st.write("Lütfen reyonun net bir fotoğrafını yükleyin. AI, SKU listesindeki ürünleri otomatik tarayacaktır.")
        
        # Fotoğraf Yükleme Alanı
        img_file = st.file_uploader("📷 Reyon Fotoğrafı Yükle", type=['png', 'jpg', 'jpeg'])

        if img_file:
            img = Image.open(img_file)
            st.image(img, caption="Analiz edilecek görsel", use_container_width=True)
            
            if st.button("🔍 ANALİZ ET VE DENETİMİ BİTİR", use_container_width=True, type="primary"):
                with st.spinner('AI Görüntü İşleniyor... Ürünler tanımlanıyor...'):
                    time.sleep(3) # Analiz süresi simülasyonu
                
                st.balloons()
                st.header("📊 Analiz Sonucu")
                
                # Burada AI sonucunu simüle ediyoruz (Gerçekte bu kısım bir modelden gelir)
                results = []
                for _, row in sku_df.iterrows():
                    # Rastgele var/yok simülasyonu (Gerçekte AI çıktısı olacak)
                    status = "✅ Mevcut" if "70cl" in row['Ürün Adı'] else "❌ Eksik"
                    results.append({"Ürün": row['Ürün Adı'], "Durum": status})
                
                res_df = pd.DataFrame(results)
                
                # Sonuçları Tablo Olarak Göster
                st.table(res_df)
                
                available_count = sum(1 for r in results if "Mevcut" in r['Durum'])
                st.metric("Bulunabilirlik Skoru", f"%{int((available_count/len(results))*100)}")
                
                st.success("Analiz tamamlandı ve merkeze raporlandı!")