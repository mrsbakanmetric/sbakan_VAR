import streamlit as st
import pandas as pd
from PIL import Image
import time

# Sayfa Yapılandırması
st.set_page_config(page_title="AI Saha Denetimi", page_icon="🥃", layout="centered")

# --- GELİŞMİŞ ŞIK TASARIM (CSS) ---
st.markdown("""
    <style>
    /* Ana Başlık */
    .main-title { font-size: 30px; font-weight: bold; text-align: center; color: #1E1E1E; margin-bottom: 10px; }
    
    /* Skor Kartı Tasarımı */
    .score-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 5px solid #FF4B4B;
        margin: 20px 0px;
    }
    .score-value { font-size: 50px; font-weight: bold; color: #FF4B4B; }
    .score-label { font-size: 18px; color: #666; text-transform: uppercase; letter-spacing: 1px; }

    /* Sidebar Tablo Küçültme */
    .stTable { font-size: 12px !important; }
    
    /* Butonları Güzelleştir */
    .stButton > button { 
        height: 3.5em; 
        border-radius: 12px; 
        font-weight: bold; 
        transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. SKU YÜKLEME VE LİSTELEME (SİDEBAR) ---
with st.sidebar:
    st.subheader("⚙️ SKU Yönetimi")
    uploaded_sku = st.file_uploader("Yeni Liste Yükle", type=['xlsx', 'csv'])
    
    # Veriyi belirle
    if uploaded_sku:
        sku_df = pd.read_csv(uploaded_sku) if uploaded_sku.name.endswith('.csv') else pd.read_excel(uploaded_sku)
        st.success("Yeni Liste Aktif")
    else:
        # Varsayılan Liste
        sku_df = pd.DataFrame({"Kontrol Edilecek Ürünler": [
            "Chivas Regal 12 YO", 
            "JW Black Label", 
            "Jack Daniel's 70cl",
            "Yeni Rakı 70cl", 
            "Tekirdağ Altın Seri",
            "Beylerbeyi Göbek"
        ]})
    
    st.divider()
    st.caption("📋 AKTİF SKU LİSTESİ")
    st.table(sku_df) # Sidebar'da listeyi gösteriyoruz

# --- 2. ANA EKRAN: KANAL VE MAĞAZA ---
st.markdown('<div class="main-title">📸 AI SAHA DENETİM ASİSTANI</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    channel = st.selectbox("Kanal:", ["Migros", "Carrefour", "Metro"], index=None, placeholder="Seçiniz...")
with col_b:
    store = st.selectbox("Mağaza:", ["Ataşehir MMM", "Kozyatağı Hiper", "Güneşli Toptancı", "Beşiktaş 5M"], index=None, placeholder="Mağaza seç...")

if channel and store:
    st.divider()
    
    # --- 3. FOTOĞRAF YÜKLEME ---
    st.write("### 📸 Reyon Fotoğrafı")
    img_file = st.file_uploader("Kamerayı aç veya görsel seç", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

    if img_file:
        img = Image.open(img_file)
        st.image(img, use_container_width=True)
        
        # --- OTOMATİK ANALİZ SÜRECİ ---
        with st.status("🔍 AI Görüntü Analizi Yapılıyor...", expanded=True) as status:
            time.sleep(2) 
            st.write("SKU eşleşmeleri kontrol ediliyor...")
            time.sleep(1.5)
            status.update(label="✅ Analiz Tamamlandı!", state="complete", expanded=False)
        
        # --- SONUÇLAR VE ŞIK SKOR KARTI ---
        st.divider()
        
        # Simülasyon Mantığı
        results = []
        for p in sku_df.iloc[:, 0]:
            # Örnek: Adında '70cl' geçenler mevcut, diğerleri eksik gibi simüle et
            is_found = len(p) % 2 == 0 
            status = "✅ Mevcut" if is_found else "❌ Eksik"
            results.append({"Ürün": p, "Durum": status})
        
        res_df = pd.DataFrame(results)
        found_count = sum(1 for r in results if "Mevcut" in r['Durum'])
        score = int((found_count / len(results)) * 100)

        # Dinamik Renk Belirleme
        score_color = "#28A745" if score >= 80 else "#FFC107" if score >= 50 else "#DC3545"

        # ŞIK SKOR KARTI (HTML)
        st.markdown(f"""
            <div class="score-card" style="border-top: 8px solid {score_color};">
                <div class="score-label">Bulunabilirlik Skoru</div>
                <div class="score-value" style="color: {score_color};">%{score}</div>
                <div style="color: {score_color}; font-weight: bold;">
                    { 'MÜKEMMEL' if score >= 80 else 'GELİŞTİRİLMELİ' if score >= 50 else 'KRİTİK SEVİYE' }
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Detaylı Tablo
        st.write("### 📊 Ürün Detay Listesi")
        st.table(res_df)
        
        if st.button("🚀 DENETİMİ ONAYLA VE GÖNDER", use_container_width=True, type="primary"):
            st.balloons()
            st.toast("Veriler başarıyla merkeze iletildi.")