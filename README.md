# 🏥 AI Medical Report Analyzer

This project is an **Educational and Analysis Tool** designed to extract structural data and insights from medical reports using the "Medical Transcriptions" dataset from Kaggle.

It is **non-diagnostic**. Is developed solely to demonstrate Text Mining and Natural Language Processing (NLP) techniques.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)

## 🚀 Features

1.  **Section Parsing:**
    *   Splits report text into standard medical sections (e.g., `HISTORY`, `MEDICATIONS`, `PLAN`).
    *   Uses Regex to structure irregular and messy text formats.
2.  **Statistical Analysis:**
    *   Calculates word and sentence counts.
    *   Estimates reading time.
3.  **Keyword Extraction:**
    *   Identifies the most frequent medical terms by removing stopwords.
4.  **Interactive Interface (Streamlit):**
    *   Provides a web interface for analyzing single reports and visualizing findings from the entire dataset.

---

## 🛠 Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/umuterenakbass/ai-medical-report-analyzer.git
    cd ai-medical-report-analyzer
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Mac/Linux
    # .venv\Scripts\activate   # Windows
    ```

3.  **Install Required Libraries:**
    ```bash
    pip install pandas tqdm streamlit matplotlib
    ```

---

## 🖥 Usage

### 1. Data Inspection (CLI)
To analyze a random report in the terminal:
```bash
python src/inspect_data.py
```

### 2. Batch Analysis (CLI)
To process the entire `mtsamples.csv` file and export results:
```bash
python src/main.py mtsamples.csv results.jsonl
# You can set a limit for testing:
python src/main.py mtsamples.csv results.jsonl --limit 100
```

### 3. Web Interface (Streamlit)
To use the visual analysis tool in your browser:
```bash
streamlit run src/app.py
```
*(It will open automatically in your browser)*

---

## 📂 Project Structure

```
ai-medical-report-analyzer/
├── mtsamples.csv        # Kaggle Dataset (Raw Data)
├── results.jsonl        # Analysis Results (Output)
├── src/
│   ├── app.py           # Streamlit Web Application
│   ├── extractor.py     # Core Analysis Engine (Class)
│   ├── main.py          # Batch Processing Script (CLI)
│   ├── inspect_data.py  # Quick Test Script
│   └── analyze_insights.py # Statistical Summary
└── README.md            # Documentation
```

---

## ⚠️ Disclaimer

This software is for **educational and research purposes only**. The results extracted cannot replace a physician's opinion. It **CANNOT** be used for medical diagnosis or treatment decisions.
