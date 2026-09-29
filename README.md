# FAQ Chatbot Assistant — CodeAlpha AI Internship

An intelligent, context-aware FAQ Chatbot for e-commerce support built with **Streamlit**, **sentence-transformers**, and **NLTK**. Features semantic vector matching, 3-tier confidence thresholding, and an interactive chat interface.

![Python](https://img.shields.io/badge/Python-3.9+-18181b?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-18181b?logo=streamlit)
![SentenceTransformers](https://img.shields.io/badge/Embeddings-all--MiniLM--L6--v2-18181b)

---

## Features

- **Semantic Vector Matching**: Uses `all-MiniLM-L6-v2` dense embeddings to understand synonyms and semantic intent (e.g. recognizing *"cancel my package"* as *"cancel my order"*).
- **3-Tier Intelligent Thresholding**:
  - **Direct Match ($\ge 50\%$)**: Delivers direct, confident answers.
  - **Borderline / Clarification ($35\% - 49\%$)**: Identifies ambiguous topics and asks for user confirmation with clickable suggestions instead of hallucinating.
  - **Out-of-Domain ($< 35\%$)**: Gracefully informs the user when a query is outside the scope of e-commerce support.
- **35+ Comprehensive FAQ Pairs**: Covers Shipping & Delivery, Payments & Pricing, Returns & Refunds, Account Management, and Orders & Tracking.
- **Interactive Chat UI**: Clean, non-AI styled interface with typing animations, confidence badges, and conversation history.
- **Categorized Sidebar Explorer**: Browse frequently asked questions organized by topic.
- **100% Local & Free**: Runs locally without requiring external LLM API keys.

---

## Tech Stack

| Component | Technology |
|---|---|
| **Frontend** | Streamlit (Chat UI) |
| **Semantic Matching** | Sentence-Transformers (`all-MiniLM-L6-v2`) + PyTorch |
| **NLP Preprocessing** | NLTK (Tokenization, Stopwords, Lemmatization) |
| **Language** | Python 3.9+ |

---

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/berlin-22/code_alpha_FAQ_bot.git
   cd code_alpha_FAQ_bot
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the chatbot**
   ```bash
   streamlit run app.py
   ```

5. Open `http://localhost:8501` (or `http://localhost:8502`) in your browser.

---

## Project Structure

```
CodeAlpha_ChatbotFAQ/
├── .streamlit/
│   └── config.toml     # Minimalist theme configuration
├── app.py              # Streamlit chat interface & message handling
├── chatbot.py          # Semantic embedding matching engine & tiered logic
├── preprocessor.py     # NLTK tokenization & cleaning
├── faq_data.py         # Curated FAQ dataset (35+ Q&A pairs)
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Documentation
```

---

## How It Works

```
User Query ──► NLP Preprocessing ──► Dense Embedding (384-d) ──► Cosine Similarity
                                                                     │
               ┌───────────────────────┬─────────────────────────────┘
               ▼                       ▼                             ▼
       Score >= 50%              35% <= Score < 50%             Score < 35%
     (Direct Answer)           (Clarify / Suggest)          (Out-of-Domain Help)
```

---

## Acknowledgements

Built for the **CodeAlpha Artificial Intelligence Internship** (Task 2).
