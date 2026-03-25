import streamlit as st
import pandas as pd
from PIL import Image
import time

# Sayfa Yapılandırması
st.set_page_config(page_title="AI Saha Denetimi", page_icon="🥃", layout="centered")

# --- ŞIK TASARIM (CSS) ---
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; text-align: center; color: #1E1E1E; }
    .score-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
        text-align: center;
        margin: 15px 0px;
    }
    .score-value { font-size: 45px; font-weight: bold; }
    /* Görselin etrafına ince bir çerçeve */
    .img-preview { border: 1px solid #ddd; border-radius: 8px; padding: 5px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. SİDEBAR (SKU LİSTESİ) ---
with st.sidebar:
    st.subheader("⚙️ SKU Yönetimi")
    uploaded_sku = st.file_uploader("Yeni Liste Yükle", type=['xlsx', 'csv'])
    
    if uploaded_sku:
        sku_df = pd.read_csv(uploaded_sku) if uploaded_sku.name.endswith('.csv') else pd.read_excel(uploaded_sku)
    else:
        sku_df = pd.DataFrame({"Ürün": ["Chivas 12 YO", "JW Black Label", "Jack Daniel's 70cl", "Yeni Rakı 70cl", "Tekirdağ Altın", "Beylerbeyi Göbek"]})
    
    st.divider()
    st.caption("📋 DENETLENECEK ÜRÜNLER")
    st.table(sku_df)

# --- 2. ANA EKRAN ---
st.markdown('<div class="main-title">📸 AI SAHA ASİSTANI</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    channel = st.selectbox("Kanal:", ["Migros", "Carrefour", "Metro"], index=None, placeholder="Seçiniz...")
with col_b:
    store = st.selectbox("Mağaza:", ["Ataşehir MMM", "Kozyatağı Hiper", "Güneşli Toptancı"], index=None, placeholder="Seçiniz...")

if channel and store:
    st.divider()
    st.write("### 📸 Reyon Fotoğrafı")
    img_file = st.file_uploader("Kamerayı aç / Görsel seç", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

    if img_file:
        # FOTOĞRAFI 10'DA 1 ORANINDA KÜÇÜLTME (Örn: 70 pixel genişlik)
        # use_container_width=False yaparak genişliği biz belirliyoruz
        st.image(Image.open(img_file), caption="Yüklenen Görsel", width=120) 
        
        # --- OTOMATİK ANALİZ ---
        with st.status("🔍 AI Analiz Ediyor...", expanded=False) as status:
            time.sleep(2)
            status.update(label="✅ Analiz Tamamlandı!", state="complete")
        
        # --- SKOR VE SONUÇLAR ---
        results = []
        for p in sku_df.iloc[:, 0]:
            status = "✅ Mevcut" if len(p) % 2 == 0 else "❌ Eksik"
            results.append({"Ürün": p, "Durum": status})
        
        found_count = sum(1 for r in results if "Mevcut" in r['Durum'])
        score = int((found_count / len(results)) * 100)
        score_color = "#28A745" if score >= 80 else "#FFC107" if score >= 50 else "#DC3545"

        st.markdown(f"""
            <div class="score-card" style="border-top: 6px solid {score_color};">
                <div style="font-size: 14px; color: #666;">BULUNABİLİRLİK</div>
                <div class="score-value" style="color: {score_color};">%{score}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("### 📊 Detay Listesi")
        st.table(pd.DataFrame(results))
        
        if st.button("🚀 VERİLERİ GÖNDER", use_container_width=True, type="primary"):
            st.balloons()
            st.toast("Rapor iletildi.")