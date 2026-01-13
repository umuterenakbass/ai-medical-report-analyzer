import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

# Proje ana dizinini Python yoluna ekle (src modülünü bulabilmesi için)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.extractor import MedicalReportExtractor

st.set_page_config(page_title="Tıbbi Rapor Analizcisi", layout="wide")

st.title("🏥 AI Medical Report Analyzer")
st.markdown("Kaggle 'Medical Transcriptions' veri seti üzerinde non-diagnostik analizler.")

# 1. Kenar Çubuğu - Dosya Yükleme & Ayarlar
st.sidebar.header("Veri ve Ayarlar")

uploaded_file = st.sidebar.file_uploader("Bir metin dosyası yükle...", type=["txt"])
action = st.sidebar.radio("Ne yapmak istersin?", ["Tek Rapor Analizi", "Toplu İstatistikler (CSV)"])

extractor = MedicalReportExtractor()

# --- MOD 1: TEK RAPOR ANALİZİ ---
if action == "Tek Rapor Analizi":
    input_text = ""
    
    if uploaded_file is not None:
        # Dosyayı oku
        input_text = uploaded_file.read().decode("utf-8")
    else:
        # Örnek metin
        st.info("Kendi dosyanı yükleyebilir veya aşağıdaki örnek metni düzenleyebilirsin.")
        input_text = st.text_area("Rapor Metni:", height=300, value="""CHIEF COMPLAINT: Chest pain.
HISTORY: The patient is a 55-year-old male presenting with chest pain for 2 days.
MEDICATIONS: Aspirin, Metoprolol.
ALLERGIES: Penicillin.
PLAN: EKG, cardiac enzymes, cardiology consult.""")

    if st.button("Analiz Et"):
        if not input_text.strip():
            st.warning("Lütfen analiz edilecek bir metin gir.")
        else:
            with st.spinner("Analiz ediliyor..."):
                # Analizleri çağır
                sections = extractor.extract_sections(input_text)
                metrics = extractor.calculate_metrics(input_text)
                keywords = extractor.extract_keywords(input_text)

                # Sonuçları Göster
                col1, col2, col3 = st.columns(3)
                col1.metric("Kelime Sayısı", metrics['word_count'])
                col2.metric("Okuma Süresi (sn)", metrics['reading_time_sec'])
                col3.metric("Cümle Sayısı", metrics['sentence_count'])
                
                # İki kolonlu yapı: Sol (Metin), Sağ (Analiz Detayları)
                c_left, c_right = st.columns([2, 1])
                
                with c_left:
                    st.subheader("📝 Ayrıştırılan Bölümler")
                    if sections:
                        for header, content in sections.items():
                            with st.expander(header, expanded=True):
                                st.write(content)
                    else:
                        st.warning("Bölüm başlıkları tespit edilemedi.")

                with c_right:
                    st.subheader("🔑 Öne Çıkan Kelimeler")
                    st.write(", ".join([f"**{w}** ({c})" for w, c in keywords]))
                    
                    st.subheader("Ham Metin")
                    st.text_area("Original", input_text, height=150, disabled=True)

# --- MOD 2: TOPLU İSTATİSTİKLER (Mevcut results.jsonl üzerinden) ---
elif action == "Toplu İstatistikler (CSV)":
    results_path = "results.jsonl"
    
    if os.path.exists(results_path):
        # JSONL yükle
        data = []
        with open(results_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line))
        df = pd.DataFrame(data)
        
        # Metrikleri parse et
        metrics_df = pd.json_normalize(df['metrics'])
        df = pd.concat([df.drop(['metrics'], axis=1), metrics_df], axis=1)
        
        st.success(f"{len(df)} raporun analiz sonuçları yüklendi.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("En Uzun Raporlar (Kelime)")
            st.bar_chart(df[['specialty', 'word_count']].sort_values('word_count', ascending=False).head(10).set_index('specialty'))
            
        with col2:
            st.subheader("Uzmanlık Dağılımı")
            st.bar_chart(df['specialty'].value_counts().head(10))
            
        st.subheader("Veri Seti Önizleme")
        st.dataframe(df.head(20))
        
    else:
        st.error(f"'{results_path}' dosyası bulunamadı. Lütfen önce terminalden 'python src/main.py' komutunu çalıştırın.")
