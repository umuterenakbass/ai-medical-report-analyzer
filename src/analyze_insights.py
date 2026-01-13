import pandas as pd
import json
import matplotlib.pyplot as plt

def analyze_results(results_file):
    print(f"Sonuçlar yükleniyor: {results_file}...")
    
    # JSONL dosyasını Pandas DataFrame'e çevir
    data = []
    with open(results_file, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
            
    df = pd.DataFrame(data)
    
    print(f"Toplam Analiz Edilen Rapor: {len(df)}")
    
    # 1. Metrikleri (Word Count vb.) ayrı sütunlara çıkaralım
    # JSON içindeki 'metrics' alanını düzleştirelim (flatten)
    metrics_df = pd.json_normalize(df['metrics'])
    df = pd.concat([df.drop(['metrics'], axis=1), metrics_df], axis=1)
    
    # --- ANALİZLER ---
    
    print("\n1. EN UZUN RAPORLAR (Kelime Sayısına Göre):")
    print(df[['id', 'specialty', 'word_count']].sort_values('word_count', ascending=False).head(5))
    
    print("\n2. ORTALAMA OKUMA SÜRESİ (Saniye):")
    avg_time = df['reading_time_sec'].mean()
    print(f"{avg_time:.2f} saniye")
    
    print("\n3. EN SIK RASTLANAN BÖLÜMLER:")
    # Tüm listeleri tek bir liste haline getir (explode) ve say
    all_sections = df.explode('sections')['sections']
    print(all_sections.value_counts().head(5))
    
    print("\n4. UZMANLIK ALANLARINA GÖRE ORTALAMA KELİME SAYISI:")
    print(df.groupby('specialty')['word_count'].mean().sort_values(ascending=False).head(5))

if __name__ == "__main__":
    analyze_results("results.jsonl")
