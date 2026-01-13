import pandas as pd
import json
import argparse
import sys
import os
from tqdm import tqdm  # İlerleme çubuğu için

# Modül import sorunu için
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.extractor import MedicalReportExtractor

def main():
    # 1. Komut Satırı Argümanlarını Ayarla
    parser = argparse.ArgumentParser(description="Tıbbi Rapor Analizcisi (CSV -> JSONL)")
    parser.add_argument("input_csv", help="Giriş yapılacak CSV dosyasının yolu")
    parser.add_argument("output_file", help="Sonuçların kaydedileceği dosya yolu (.jsonl)")
    parser.add_argument("--limit", type=int, help="Test için sadece ilk N satırı işle", default=None)
    
    args = parser.parse_args()
    
    # 2. İşleyici Sınıfı Başlat
    extractor = MedicalReportExtractor()
    
    # 3. CSV Dosyasını Yükle
    print(f"Veri yükleniyor: {args.input_csv}...")
    try:
        df = pd.read_csv(args.input_csv)
    except FileNotFoundError:
        print("Hata: CSV dosyası bulunamadı.")
        return

    # Boş verileri temizle
    df = df.dropna(subset=['transcription'])
    
    # Limit varsa uygula
    if args.limit:
        df = df.head(args.limit)
        print(f"Uyarı: Sadece ilk {args.limit} satır işlenecek.")
    
    total_records = len(df)
    print(f"Analiz edilecek rapor sayısı: {total_records}")
    
    # 4. Analiz Döngüsü
    results = []
    
    # tqdm ile ilerleme çubuğu gösterelim
    for index, row in tqdm(df.iterrows(), total=total_records, desc="Analiz ediliyor"):
        
        text = str(row['transcription'])
        
        # Analizleri yap
        sections = extractor.extract_sections(text)
        metrics = extractor.calculate_metrics(text)
        keywords = extractor.extract_keywords(text)
        
        # Sonuç objesini oluştur
        result = {
            "id": index, # CSV'deki satır numarası
            "specialty": row['medical_specialty'],
            "metrics": metrics,
            "keywords": [k[0] for k in keywords], # Sadece kelimelerin kendisini al
            "sections": list(sections.keys()) # Sadece bulunan başlıkları kaydet (yer kaplamasın diye)
        }
        
        results.append(result)

    # 5. Sonuçları Kaydet (JSONL formatında)
    print(f"Sonuçlar kaydediliyor: {args.output_file}...")
    with open(args.output_file, 'w', encoding='utf-8') as f:
        for entry in results:
            json.dump(entry, f)
            f.write('\n') # Her yeni JSON bir alt satıra
            
    print("✅ İşlem tamamlandı!")

if __name__ == "__main__":
    main()
