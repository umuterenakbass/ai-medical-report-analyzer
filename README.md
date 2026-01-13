# 🏥 AI Medical Report Analyzer

Bu proje, Kaggle üzerindeki "Medical Transcriptions" veri setini kullanarak tıbbi raporlardan yapısal veriler ve içgörüler (insights) çıkarmayı amaçlayan bir **Eğitim ve Analiz Aracıdır**.

Hiçbir teşhis koymaz (Non-diagnostic). Sadece metin madenciliği (Text Mining) ve doğal dil işleme (NLP) yöntemlerini öğretmek amacıyla geliştirilmiştir.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)

## 🚀 Özellikler

1.  **Bölüm Ayrıştırma (Section Parsing):**
    *   Rapor metnini klasik başlıklarına ayırır (örn. `HISTORY`, `MEDICATIONS`, `PLAN`).
    *   Regex kullanarak düzensiz metinleri yapılandırır.
2.  **İstatistiksel Analiz:**
    *   Kelime ve cümle sayıları.
    *   Tahmini okuma süresi hesaplama.
3.  **Anahtar Kelime Çıkarımı (Keyword Extraction):**
    *   Etkisiz kelimeleri (Stopwords) temizleyerek en sık geçen tıbbi terimleri bulur.
4.  **İnteraktif Arayüz (Streamlit):**
    *   Hem tekil raporları analiz etmek hem de toplu veri setini görselleştirmek için web arayüzü sunar.

---

## 🛠 Kurulum

1.  **Repo'yu Klonlayın:**
    ```bash
    git clone https://github.com/umuterenakbass/ai-medical-report-analyzer.git
    cd ai-medical-report-analyzer
    ```

2.  **Sanal Ortam Oluşturun (Önerilen):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Mac/Linux
    # .venv\Scripts\activate   # Windows
    ```

3.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install pandas tqdm streamlit matplotlib
    ```

---

## 🖥 Kullanım

### 1. Veri İnceleme (CLI)
Rastgele bir raporu terminalde analiz etmek için:
```bash
python src/inspect_data.py
```

### 2. Toplu Analiz (CLI)
Tüm `mtsamples.csv` dosyasını işleyip sonuçları dışarı aktarmak için:
```bash
python src/main.py mtsamples.csv results.jsonl
# Test için limit koyabilirsiniz:
python src/main.py mtsamples.csv results.jsonl --limit 100
```

### 3. Web Arayüzü (Streamlit)
Analiz aracını tarayıcıda görsel olarak kullanmak için:
```bash
streamlit run src/app.py
```
*(Tarayıcınızda otomatik olarak açılacaktır)*

---

## 📂 Proje Yapısı

```
ai-medical-report-analyzer/
├── mtsamples.csv        # Kaggle Veri Seti (Raw Data)
├── results.jsonl        # Analiz Sonuçları (Output)
├── src/
│   ├── app.py           # Streamlit Web Uygulaması
│   ├── extractor.py     # Ana Analiz Motoru (Class)
│   ├── main.py          # Toplu İşleme Scripti (CLI)
│   ├── inspect_data.py  # Hızlı Test Scripti
│   └── analyze_insights.py # İstatistik Özeti
└── README.md            # Dokümantasyon
```

---

## ⚠️ Yasal Uyarı

Bu yazılım sadece **eğitim ve araştırma** amaçlıdır. Çıkarılan sonuçlar, bir doktorun görüşünün yerini tutamaz. Tıbbi teşhis veya tedavi amacıyla **KULLANILAMAZ**.
