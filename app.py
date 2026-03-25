{\rtf1\ansi\ansicpg1252\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww33660\viewh21120\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import datetime\
\
# 1. Veri Yap\uc0\u305 s\u305 : Her kanal\u305 n kendine \'f6zel ma\u287 azalar\u305  ve \'fcr\'fcn listesi (Assortment)\
channels = \{\
    "Migros": \{\
        "stores": ["Ata\uc0\u351 ehir MMM", "Caddebostan Jet", "Be\u351 ikta\u351  5M"],\
        "assortment": ["Efes Pilsen 50cl", "Miller 33cl", "Budweiser 50cl"]\
    \},\
    "CarrefourSA": \{\
        "stores": ["\uc0\u304 stinye Hiper", "Kozyata\u287 \u305  Gurme", "Ac\u305 badem S\'fcper"],\
        "assortment": ["Bomonti Filtresiz", "Becks 33cl", "Corona 35.5cl"]\
    \},\
    "Metro": \{\
    "stores": ["G\'fcne\uc0\u351 li Toptanc\u305 ", "Kozyata\u287 \u305  Toptanc\u305 "],\
    "assortment": ["Efes \'d6zel Seri", "Carlsberg 50cl", "Weihenstephaner"]\
    \}\
\}\
\
st.title("\uc0\u55357 \u57057 \u65039  FMCG B2B Saha Sat\u305 \u351  Denetimi")\
st.sidebar.header("Kullan\uc0\u305 c\u305  Paneli")\
st.sidebar.info("Temsilci: Ahmet Y\uc0\u305 lmaz")\
\
# ADIM 1: Kanal Se\'e7imi\
channel_choice = st.selectbox("Denetim yap\uc0\u305 lacak kanal\u305  se\'e7in:", ["Se\'e7iniz"] + list(channels.keys()))\
\
if channel_choice != "Se\'e7iniz":\
    # ADIM 2: Ma\uc0\u287 aza Se\'e7imi\
    store_choice = st.selectbox(f"\{channel_choice\} Ma\uc0\u287 azas\u305  se\'e7in:", channels[channel_choice]["stores"])\
    \
    st.divider()\
    st.subheader(f"\uc0\u55357 \u56523  \{store_choice\} - Portf\'f6y Kontrol\'fc")\
    \
    # ADIM 3: Assortment Check (Bulunabilirlik)\
    st.write("Rafta **BULUNAN** \'fcr\'fcnleri i\uc0\u351 aretleyin:")\
    check_results = \{\}\
    for product in channels[channel_choice]["assortment"]:\
        check_results[product] = st.checkbox(product, value=True)\
    \
    st.divider()\
    \
    # ADIM 4: Foto\uc0\u287 raf Y\'fckleme\
    st.subheader("\uc0\u55357 \u56567  Raf Foto\u287 raf\u305 ")\
    uploaded_file = st.file_uploader("Reyonun foto\uc0\u287 raf\u305 n\u305  \'e7ekin veya y\'fckleyin", type=['png', 'jpg', 'jpeg'])\
    \
    if uploaded_file is not None:\
        st.image(uploaded_file, caption='Y\'fcklenen Raf G\'f6rseli', use_column_width=True)\
        st.success("G\'f6r\'fcnt\'fc ba\uc0\u351 ar\u305 yla y\'fcklendi. AI analizi i\'e7in haz\u305 r.")\
\
    # ADIM 5: Kaydetme\
    if st.button("Denetimi Tamamla ve G\'f6nder"):\
        # Veriyi bir JSON/S\'f6zl\'fck yap\uc0\u305 s\u305 nda topluyoruz (Veritaban\u305 na gidecek veri)\
        audit_data = \{\
            "tarih": str(datetime.datetime.now()),\
            "kanal": channel_choice,\
            "magaza": store_choice,\
            "bulunabilirlik": check_results,\
            "gorsel_durumu": "Y\'fcklendi" if uploaded_file else "Eksik"\
        \}\
        st.balloons()\
        st.json(audit_data) # Geli\uc0\u351 tirici i\'e7in veriyi ekrana basar\
        st.success("Veriler merkeze ba\uc0\u351 ar\u305 yla iletildi!")}