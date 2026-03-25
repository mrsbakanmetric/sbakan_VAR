import streamlit as st
import pandas as pd
from PIL import Image
import time

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
    </style>
    """, unsafe_allow_html=True)

# --- 1. SİDEBAR: DİNAMİK PORTFÖY YÖNETİMİ ---
with st.sidebar:
    st.subheader("⚙️ Portföy Yönetimi")
    st.caption("Ürün eklemek için listenin altına yazın. Silmek için satırı seçip 'Delete' tuşuna basın.")
    
    if 'sku_list' not in st.session_state:
        st.session_state.sku_list = pd.DataFrame([
            {"Ürün Adı": "Chivas Regal 12 YO"},
            {"Ürün Adı": "JW Black Label"},
            {"Ürün Adı": "Jack Daniel's 70cl"},
            {"Ürün Adı": "Yeni Rakı 70cl"},
            {"Ürün Adı": "Tekirdağ Altın Seri"},
            {"Ürün Adı": "Beylerbeyi Göbek"}
        ])

    # DİNAMİK EDİTÖR: Satır ekleme ve silme (yanında checkbox/silme mantığı ile) aktif
    edited_sku = st.data_editor(
        st.session_state.sku_list,
        num_rows="dynamic", # Bu parametre satır ekleme/silme izni verir
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
    if st.button("🍊 Migros", use_container_width=True):
        st.session_state.selected_channel = "Migros"
with c2:
    if st.button("🔵 Carrefour", use_container_width=True):
        st.session_state.selected_channel = "Carrefour"
with c3:
    if st.button("⚪ Metro", use_container_width=True):
        st.session_state.selected_channel = "Metro"

# Mağaza Verileri
stores_data = {
    "Migros": ["Ataşehir MMM", "Beşiktaş 5M", "Caddebostan Jet", "Mecidiyeköy MMM"],
    "Carrefour": ["İstinye Hiper", "Kozyatağı Gurme", "Acıbadem Süper"],
    "Metro": ["Güneşli Toptancı", "Kozyatağı Toptancı", "Ayazağa Toptancı"]
}

# --- 3. MAĞAZA VE ANALİZ AKIŞI ---
if st.session_state.selected_channel:
    ch = st.session_state.selected_channel
    st.divider()
    st.write(f"### 2. {ch} Mağaza Seçimi")
    
    store_choice = st.selectbox(
        "Denetlenecek mağazayı seçin:",
        options=stores_data[ch],
        index=None,
        placeholder="Mağaza ara..."
    )

    if store_choice:
        st.divider()
        st.write("### 3. Reyon Fotoğrafı")
        img_file = st.file_uploader("Görsel yükle (AI Analizi otomatik başlar)", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

        if img_file:
            # 10'da 1 oranında küçültülmüş önizleme
            st.image(Image.open(img_file), caption="Yüklenen Görsel", width=120) 
            
            # --- YÜZDESEL PROGRESS BAR ANALİZİ ---
            st.write("🔍 **AI Görüntü İşleme Başlatıldı...**")
            progress_bar = st.progress(0)
            status_text = st.empty()

            for percent_complete in range(0, 101, 10):
                time.sleep(0.3) # Analiz hızı simülasyonu
                progress_bar.progress(percent_complete)
                status_text.text(f"Analiz ediliyor: %{percent_complete} tamamlandı")
            
            status_text.success("✅ Analiz Başarıyla Tamamlandı!")
            
            # Sonuçları Hesapla
            results = []
            current_skus = st.session_state.sku_list["Ürün Adı"].tolist()
            for p in current_skus:
                if p:
                    # Basit simülasyon mantığı
                    status = "✅ Mevcut" if len(p) % 2 == 0 else "❌ Eksik"
                    results.append({"Ürün": p, "Durum": status})
            
            if results:
                found_count = sum(1 for r in results if "Mevcut" in r['Durum'])
                score = int((found_count / len(results)) * 100)
                score_color = "#28A745" if score >= 80 else "#FFC107" if score >= 50 else "#DC3545"

                st.markdown(f"""
                    <div class="score-card" style="border-top: 6px solid {score_color};">
                        <div style="font-size: 14px; color: #666;">GENEL BULUNABİLİRLİK</div>
                        <div class="score-value" style="color: {score_color};">%{score}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.table(pd.DataFrame(results))
                
                if st.button("🚀 RAPORU ONAYLA VE GÖNDER", use_container_width=True, type="primary"):
                    st.balloons()
                    st.toast("Veriler veritabanına işlendi.")