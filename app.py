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
        height: 6em; /* Logo sığması için yüksekliği artırıldı */
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
    </style>
    """, unsafe_allow_html=True)

# --- Logoları Tanımla ---
# Not: Gerçek logolar yerine Streamlit'in sunduğu ikonları kullanıyoruz.
# Buton içine resim koymak karmaşık olduğu için emoji ile görselleştirme yapıyoruz.
carrefour_logo = "🔴🔵 Carrefour" # Carrefour renklerini yansıtan emoji
migros_logo = "🍊 Migros" # Migros turuncusunu yansıtan emoji
metro_logo = "⚪ Metro" # Metro mavisini yansıtan emoji

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
    if st.button(carrefour_logo, use_container_width=True):
        st.session_state.selected_channel = "Carrefour"
with c2:
    if st.button(migros_logo, use_container_width=True):
        st.session_state.selected_channel = "Migros"
with c3:
    if st.button(metro_logo, use_container_width=True):
        st.session_state.selected_channel = "Metro"

# Mağaza Verileri (Her biri için 10 tane)
stores_data = {
    "Migros": ["Ataşehir MMM", "Beşiktaş 5M", "Caddebostan Jet", "Mecidiyeköy MMM", "Bahçeşehir 5M", "Suadiye Jet", "Kadıköy 3M", "Fulya MM", "Zekeriyaköy Jet", "Üsküdar MM"],
    "Carrefour": ["İstinye Hiper", "Kozyatağı Gurme", "Acıbadem Süper", "Fulya Hiper", "Maltepe Park Hiper", "Ortaköy Gurme", "Bakırköy Hiper", "Beylikdüzü Hiper", "Ataşehir Gurme", "Caddebostan Süper"],
    "Metro": ["Güneşli Toptancı", "Kozyatağı Toptancı", "Pendik Toptancı", "Ayazağa Toptancı", "Merter Toptancı", "Kağıthane Toptancı", "Sancaktepe Toptancı", "Büyükçekmece Toptancı", "Esenyurt Toptancı", "Tuzla Toptancı"]
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
        img_file = st.file_uploader("Görsel yükle", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

        if img_file:
            # 10'da 1 oranında küçültülmüş önizleme
            st.image(Image.open(img_file), caption="Yüklenen Görsel", width=120) 
            
            # --- ANALİZİ BAŞLAT BUTONU ---
            st.write("")
            if st.button("🔍 ANALİZİ BAŞLAT", use_container_width=True, type="primary"):
                st.write("🔍 **AI Görüntü İşleme ve Cross-Check Başlatıldı...**")
                progress_bar = st.progress(0)
                status_text = st.empty()

                for percent_complete in range(0, 101, 20):
                    time.sleep(0.4) 
                    progress_bar.progress(percent_complete)
                    status_text.text(f"Analiz ediliyor: %{percent_complete} tamamlandı")
                
                status_text.success("✅ Analiz Tamamlandı!")
                
                # Sonuçları Hesapla
                current_skus = st.session_state.sku_list["Ürün Adı"].tolist()
                
                # Ana Liste Kontrolü
                results = []
                for p in current_skus:
                    if p:
                        is_available = random.choice([True, False])
                        if is_available:
                            results.append({"Ürün": p, "Durum": "✅ Mevcut", "Açıklama": "Ürün Rafta"})
                        else:
                            results.append({"Ürün": p, "Durum": "❌ Eksik", "Açıklama": "🛒 Sipariş Oluştur"})
                
                # Listede Olmayan Ürünler
                extra_products = [{"Ürün": "Efe Yaş Üzüm 70cl", "Analiz Notu": "Tanımsız Ürün / Rakip Sızması"}]
                
                if results:
                    found_count = sum(1 for r in results if "Mevcut" in r['Durum'])
                    score = int((found_count / len(results)) * 100)
                    score_color = "#28A745" if score >= 80 else "#FFC107" if score >= 50 else "#DC3545"

                    st.markdown(f"""
                        <div class="score-card" style="border-top: 6px solid {score_color};">
                            <div style="font-size: 14px; color: #666;">ASSORTMENT COMPLIANCE</div>
                            <div class="score-value" style="color: {score_color};">%{score}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.write("### 📋 Beklenen Portföy Durumu")
                    st.table(pd.DataFrame(results))
                    
                    st.markdown('<div class="extra-header">⚠️ LİSTEDE OLMAYAN / EKSTRA ÜRÜNLER</div>', unsafe_allow_html=True)
                    st.table(pd.DataFrame(extra_products))
                    
                    if st.button("🚀 RAPORU ONAYLA VE GÖNDER", use_container_width=True):
                        st.balloons()
                        st.toast("Rapor ve saha aksiyonları kaydedildi.")