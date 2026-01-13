import re
from collections import Counter

class MedicalReportExtractor:
    def __init__(self):
        # Genellikle kullanılan bölüm başlıkları listesi.
        # Bu listeyi zamanla genişletebiliriz.
        self.common_headers = [
            "HISTORY", "HISTORY OF PRESENT ILLNESS", "PAST MEDICAL HISTORY",
            "MEDICATIONS", "ALLERGIES", "PHYSICAL EXAMINATION", "REVIEW OF SYSTEMS",
            "ASSESSMENT", "PLAN", "DIAGNOSIS", "IMPRESSION", "CHIEF COMPLAINT",
            "PREOPERATIVE DIAGNOSES", "POSTOPERATIVE DIAGNOSES", "PROCEDURE PERFORMED"
        ]

        # Basit bir Stopwords listesi (İngilizce)
        # Bu kelimeleri analizden çıkaracağız çünkü çok sık geçiyorlar ama az bilgi taşıyorlar.
        self.stopwords = {
            "the", "and", "of", "to", "in", "a", "is", "was", "for", "with", "that", "on", "it", 
            "at", "by", "from", "as", "be", "are", "have", "has", "had", "this", "or", "an",
            "not", "but", "we", "he", "she", "patient", "history", "report", "examination",
            "left", "right", "normal", "pain", "mg", "placed", "using", "procedure", "then"
        }
        
    def extract_sections(self, text):
        """
        Metni tarar ve başlık: içerik şeklinde bir sözlük (dictionary) döndürür.
        Örn: {'HISTORY': 'Hasta 3 gündür hasta...', 'PLAN': 'İlaç verilecek.'}
        """
        sections = {}
        
        # Eğer metin boşsa boş dön
        if not text or not isinstance(text, str):
            print("Uyarı: Metin boş veya geçersiz.")
            return sections

        # Temizlik: \r karakterlerini temizle
        text = text.replace('\r', '')

        # Regex (Desen) Mantığı:
        # ^ -> Satır başı (veya öncesinde yeni satır)
        # ([A-Z ]+) -> BÜYÜK HARFLER ve BOŞLUKLARDAN oluşan bir grup (Başlık Adayı)
        # : -> İki nokta üst üste
        # Regex Açıklaması:
        # (?P<header>...) -> header isminde bir grup yakala
        # [A-Z][A-Z\s/-]+ -> Baş harfi büyük, kalanı büyük harf/boşluk/tire
        # : -> Mutlaka iki nokta üst üste ile bitsin (Virgülü kaldırdık çünkü riskli)
        # Bu pattern artık satır içi (inline) başlıkları da yakalar.
        pattern = re.compile(r'(?P<header>[A-Z][A-Z\s/-]+):')
        
        matches = list(pattern.finditer(text))
        
        # Hiç başlık bulamazsa tüm metni "UNKOWN" olarak kaydet
        if not matches:
            return {"UNKNOWN_SECTION": text.strip()}

        for i, match in enumerate(matches):
            header = match.group('header').strip()
            
            # Başlığın bittiği yer -> İçeriğin başlangıcı
            start_index = match.end()
            
            # İçeriğin bittiği yer -> Bir sonraki başlığın başladığı yer
            # Eğer son başlıksak, metnin sonuna kadar git.
            if i + 1 < len(matches):
                end_index = matches[i + 1].start()
            else:
                end_index = len(text)
            
            content = text[start_index:end_index].strip()
            
            # Gereksiz virgüle veya noktalama ile başlıyorsa temizle (Veride bazen ":," oluyor)
            content = content.lstrip(':, ')
            
            # Elde ettiğimiz bölümü kaydet
            if content: # Sadece içeriği doluysa ekle
                sections[header] = content
                
        return sections

    def calculate_metrics(self, text):
        """
        Metin istatistiklerini hesaplar: Kelime sayısı, cümle sayısı, okuma süresi.
        """
        if not text:
            return {
                "word_count": 0,
                "sentence_count": 0,
                "reading_time_sec": 0
            }
        
        # Kelime Sayısı (Boşluklara göre böl)
        words = text.split()
        word_count = len(words)
        
        # Cümle Sayısı (Basitçe nokta, ünlem ve soru işaretine göre ayır)
        sentences = re.split(r'[.!?]+', text)
        # Boş stringleri listeden temizle
        sentences = [s for s in sentences if s.strip()]
        sentence_count = len(sentences)
        
        # Okuma Süresi (Ortalama bir insan dakikada 200 kelime okur)
        words_per_minute = 200
        reading_time_sec = (word_count / words_per_minute) * 60
        
        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "reading_time_sec": round(reading_time_sec, 2)
        }

    def extract_keywords(self, text, top_n=5):
        """
        Metin içindeki en sık geçen 'anlamlı' kelimeleri bulur.
        """
        if not text:
            return []

        # 1. Metni temizle: Sadece harfler kalsın, küçük harfe çevir
        # [^a-zA-Z\s] -> Harf ve boşluk dışındaki her şeyi (noktalama vb.) sil
        clean_text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
        
        # 2. Kelimelere ayır
        words = clean_text.split()
        
        # 3. Anlamsız kelimeleri (stopwords) ve çok kısa kelimeleri filtrele
        meaningful_words = [
            w for w in words 
            if w not in self.stopwords and len(w) > 2
        ]
        
        # 4. En çok geçenleri say
        word_counts = Counter(meaningful_words)
        
        # 5. En popüler N tanesini döndür
        return word_counts.most_common(top_n)
