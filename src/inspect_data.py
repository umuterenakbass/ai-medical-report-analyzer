import pandas as pd
import sys
import os

# Proje ana dizinini Python yoluna ekle (src modülünü bulabilmesi için)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.extractor import MedicalReportExtractor

def inspect_csv(file_path):
    """
    CSV dosyasını yükler ve veri setini anlamamız için ekrana bilgiler basar.
    """
    try:
        # 1. Veriyi Oku
        df = pd.read_csv(file_path)
        
        # 2. Extractor'ı Hazırla
        extractor = MedicalReportExtractor()
        
        # 3. Rastgele Bir Rapor Seç ve Analiz Et
        sample_df = df.dropna(subset=['transcription'])
        
        if not sample_df.empty:
            sample_row = sample_df.sample(1).iloc[0] # Rastgele 1 tane seç
            raw_text = sample_row['transcription']
            
            print("\n=== ÖRNEK RAPOR İNCELEMESİ ===")
            print(f"Uzmanlık Alanı: {sample_row['medical_specialty']}")
            print("-" * 50)
            
            # --- YENİ KISIM: İstatistikler ---
            metrics = extractor.calculate_metrics(raw_text)
            print("\nRAPOR İSTATİSTİKLERİ:")
            print(f"Kelime Sayısı: {metrics['word_count']}")
            print(f"Cümle Sayısı: {metrics['sentence_count']}")
            print(f"Tahmini Okuma Süresi: {metrics['reading_time_sec']} saniye")

            # --- YENİ KISIM: Anahtar Kelimeler ---
            keywords = extractor.extract_keywords(raw_text)
            print("\nÖNE ÇIKAN KELİMELER:")
            print(", ".join([f"{word} ({count})" for word, count in keywords]))

            # --- YENİ KISIM: Ayrıştırma İşlemi ---
            print("\nAYRIŞTIRILAN BÖLÜMLER:")
            sections = extractor.extract_sections(raw_text)
            
            if sections:
                for header, content in sections.items():
                    print(f"\n[BASLIK]: {header}")
                    # İçerik çok uzunsa ilk 100 karakteri gösterelim
                    preview = content[:100] + "..." if len(content) > 100 else content
                    print(f"[ICERIK]: {preview}")
            else:
                print("Hic bolum ayristirilamadi. Ham metin gosteriliyor:")
                print(raw_text[:200])
            
            print("-" * 50)
        else:
            print("\nUyarı: 'transcription' sütunu dolu olan hiç satır bulunamadı.")
            
    except FileNotFoundError:
        print(f"Hata: '{file_path}' dosyası bulunamadı. Lütfen dosyanın proje ana dizininde olduğundan emin ol.")

if __name__ == "__main__":
    # Kod doğrudan çalıştırıldığında burası çalışır
    inspect_csv("mtsamples.csv")
