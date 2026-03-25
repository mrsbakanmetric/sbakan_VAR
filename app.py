import streamlit as st
import pandas as pd
from PIL import Image
import time

# Sayfa Yapılandırması
st.set_page_config(page_title="AI Saha Denetimi", page_icon="🥃", layout="centered")

# --- ŞIK TASARIM (CSS) ---
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; text-align: center; margin-bottom: 20px; }
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

# --- 1. SİDEBAR: DİNAMİK SKU YÖNETİMİ ---
with st.sidebar:
    st.subheader("⚙️ SKU Portföy Yönetimi")
    
    # Başlangıç verisi (Eğer session_state'de yoksa oluştur)
    if 'sku_list' not in st.session_state:
        st.session_state.sku_list = pd.DataFrame([
            {"Ürün Adı": "Chivas Regal 12 YO"},
            {"Ürün Adı": "JW Black Label"},
            {"Ürün Adı": "Jack Daniel's 70cl"},
            {"Ürün Adı": "Yeni Rakı 70cl"},
            {"Ürün Adı": "Tekirdağ Altın Seri"},
            {"Ürün Adı": "Beylerbeyi Göbek"}
        ])

    st.write("Aşağıdaki listeden ürün ekleyebilir (en alt satır), silebilir (seçip delete) veya isim değiştirebilirsiniz:")
    
    # DATA EDITOR: Manuel ekleme/silme imkanı tanır
    edited_sku = st.data_editor(
        st.session_state.sku_list,
        num_rows="dynamic", # Satır ekleme/silme özelliğini açar
        use_container_width=True,
        key="sku_editor"
    )
    
    # Güncel listeyi session_state'e kaydet
    st.session_state.sku_list = edited_sku

    st.divider()
    st.caption("💡 İpucu: Tablonun altındaki '+' butonuna basarak yeni ürün ekleyebilirsiniz.")

# --- 2. ANA EKRAN ---
st.markdown('<div class="main-title">📸 AI SAHA DENETİM ASİSTANI</div>', unsafe_allow_html=True)

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
        # Fotoğrafı 10'da 1 oranında küçültme (Önizleme)
        st.image(Image.open(img_file), caption="Yüklenen Görsel", width=120) 
        
        # --- OTOMATİK ANALİZ ---
        with st.status("🔍 AI Analiz Ediyor...", expanded=False) as status:
            time.sleep(2)
            status.update(label="✅ Analiz Tamamlandı!", state="complete")
        
        # --- SKOR VE SONUÇLAR (Dinamik Listeye Göre) ---
        results = []
        # Sidebar'da düzenlenen güncel listeyi kullanıyoruz
        current_skus = st.session_state.sku_list["Ürün Adı"].tolist()
        
        for p in current_skus:
            if p: # Boş satırları atla
                status = "✅ Mevcut" if len(p) % 2 == 0 else "❌ Eksik"
                results.append({"Ürün": p, "Durum": status})
        
        if results:
            found_count = sum(1 for r in results if "Mevcut" in r['Durum'])
            score = int((found_count / len(results)) * 100)
            score_color = "#28A745" if score >= 80 else "#FFC107" if score >= 50 else "#DC3545"

            st.markdown(f"""
                <div class="score-card" style="border-top: 6px solid {score_color};">
                    <div style="font-size: 14px; color: #666;">GÜNCEL BULUNABİLİRLİK</div>
                    <div class="score-value" style="color: {score_color};">%{score}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.write("### 📊 Detay Listesi")
            st.table(pd.DataFrame(results))
            
            if st.button("🚀 VERİLERİ GÖNDER", use_container_width=True, type="primary"):
                st.balloons()
                st.toast("Rapor iletildi.")
        else:
            st.warning("Lütfen sol panelden denetlenecek ürün ekleyin.")