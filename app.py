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
    
    /* Buton Stilleri */
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
    .extra-header { color: #D9534F; font-weight: bold; margin-top: 25px; border-bottom: 2px solid #D9534F; padding-bottom: 5px; }
    
    /* Eksik ürünler için özel stil (Opsiyonel: Tabloyu renklendirmek zor olduğu için metin odaklı gidiyoruz) */
    </style>
    """, unsafe_allow_html=True)

# --- 1. SİDEBAR: DİNAMİK PORTFÖY YÖNETİMİ ---
with st.sidebar:
    st.subheader("⚙️ Portföy Yönetimi")
    
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

# --- 3. MAĞAZA VE ANALİZ ---
if st.session_state.selected_channel:
    ch = st.session_state.selected_channel
    st.divider()
    st.write(f"### 2. {ch} Mağaza Seçimi")
    store_choice = st.selectbox("Mağaza seçin:", options=stores_data[ch], index=None, placeholder="Mağaza ara...")

    if store_choice:
        st.divider()
        st.write("### 3. Reyon Fotoğrafı")
        img_file = st.file_uploader("Görsel yükle", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

        if img_file:
            st.image(Image.open(img_file), caption="Yüklenen Görsel", width=120) 
            
            if st.button("🔍 ANALİZİ BAŞLAT", use_container_width=True, type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()

                for percent_complete in range(0, 101, 25):
                    time.sleep(0.4) 
                    progress_bar.progress(percent_complete)
                    status_text.text(f"Analiz ediliyor: %{percent_complete} tamamlandı")
                
                status_text.success("✅ Analiz Tamamlandı!")
                
                # --- SONUÇ HESAPLAMA ---
                current_skus = st.session_state.sku_list["Ürün Adı"].tolist()
                results = []
                
                for p in current_skus:
                    if p:
                        is_available = random.choice([True, False])
                        if is_available:
                            results.append({"Ürün": p, "Durum": "✅ Mevcut", "Aksiyon": "-"})
                        else:
                            # EKSİK ÜRÜN İÇİN SEPET İKONU EKLEME
                            results.append({"Ürün": p, "Durum": "❌ Eksik", "Aksiyon": "🛒 Sipariş Oluştur"})
                
                # Analiz dışı (Ekstra) Ürünler
                extra_products = [{"Ürün": "Efe Yaş Üzüm 70cl", "Tespit": "Tanımsız Ürün"}]
                
                # Skor Kartı
                found_count = sum(1 for r in results if "Mevcut" in r['Durum'])
                score = int((found_count / len(results)) * 100) if results else 0
                score_color = "#28A745" if score >= 80 else "#FFC107" if score >= 50 else "#DC3545"

                st.markdown(f"""
                    <div class="score-card" style="border-top: 6px solid {score_color};">
                        <div style="font-size: 14px; color: #666;">ASSORTMENT COMPLIANCE</div>
                        <div class="score-value" style="color: {score_color};">%{score}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # --- TABLO GÖSTERİMİ ---
                st.write("### 📋 Beklenen Portföy Durumu")
                st.table(pd.DataFrame(results))
                
                st.markdown('<div class="extra-header">⚠️ LİSTEDE OLMAYAN / EKSTRA ÜRÜNLER</div>', unsafe_allow_html=True)
                st.table(pd.DataFrame(extra_products))
                
                if st.button("🚀 RAPORU TAMAMLA", use_container_width=True):
                    st.balloons()
                    st.toast("Rapor ve Sipariş Önerileri Kaydedildi.")