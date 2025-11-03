# 🏥 Health Chatbot System

A sophisticated health chatbot implementation using TF-IDF and cosine similarity for semantic question answering with confidence scoring and explanations.

## 📋 Project Overview

This system demonstrates an intelligent health question-answering chatbot with:
- **50 Health Q&A pairs** covering major diseases (dengue, malaria, COVID-19, cold, flu, diabetes, etc.)
- **TF-IDF + Cosine Similarity** for semantic matching
- **Confidence Scoring** with automatic fallback for low-confidence responses
- **Detailed Explanations** showing why each answer was selected
- **Conversation Logging** with full interaction history
- **Performance Visualization** with statistical analysis

## 📁 Project Structure

```
dlp/
├── data/
│   └── health_qa_dataset.json      # 50 Q&A pairs on health topics
├── scripts/
│   ├── health_chatbot.py           # Core chatbot implementation (TF-IDF similarity)
│   ├── interactive_chatbot.py      # Interactive interface & conversation logging
│   └── visualization.py            # Performance analysis & visualization
├── outputs/
│   ├── conversation_logs.json      # Logged conversations with responses
│   ├── query_response_analysis.json # Detailed query analysis
│   └── similarity_scores_analysis.png # Histogram and statistics visualization
└── README.md
```

## 🔧 Installation

### Requirements
- Python 3.8+
- Required packages (see below)

### Install Dependencies

```bash
pip install scikit-learn numpy matplotlib seaborn
```

**Core Dependencies:**
- `scikit-learn`: TF-IDF vectorizer and cosine similarity
- `numpy`: Numerical computations
- `matplotlib`: Visualization
- `seaborn`: Statistical visualization

## 🚀 Quick Start

### 1. Run Example Conversations
```bash
python scripts/interactive_chatbot.py
```
This generates 10 example health queries with chatbot responses and saves logs to `outputs/conversation_logs.json`.

### 2. Interactive Mode
```bash
python scripts/interactive_chatbot.py --mode interactive
```
Start a live conversation with the chatbot. Type questions and get instant responses with confidence scores.

### 3. View Analysis & Visualization
```bash
python scripts/visualization.py
```
Generates comprehensive analysis including:
- Similarity score distribution histogram
- Box plots of confidence scores
- Success rate pie chart
- Cumulative distribution
- Category analysis

### 4. Quick Demo
```bash
python scripts/health_chatbot.py
```
Runs predefined test queries to demonstrate chatbot capabilities.

## 📊 Dataset Description

The `health_qa_dataset.json` contains 50 Q&A pairs organized by health topics:

### Categories (10+ topics):
- **Dengue Fever** (4 pairs): Symptoms, prevention, treatment
- **Malaria** (4 pairs): Symptoms, prevention, treatment
- **COVID-19** (4 pairs): Overview, symptoms, prevention, treatment
- **Common Cold** (4 pairs): Overview, symptoms, prevention, treatment
- **Influenza/Flu** (4 pairs): Overview, symptoms, prevention, treatment
- **Hypertension** (3 pairs): Causes, symptoms, management
- **Diabetes** (3 pairs): Overview, symptoms, prevention
- **Asthma** (3 pairs): Overview, triggers, management
- **Heart Disease** (3 pairs): Overview, symptoms, prevention
- **Arthritis** (3 pairs): Overview, symptoms, management
- **Thyroid Disease** (3 pairs): Overview, symptoms, management
- **Mental Health** (6 pairs): Anxiety and depression management
- **Weight Management** (2 pairs): Obesity and weight control
- **Nutrition** (2 pairs): Vitamin D deficiency
- **Sleep Disorders** (2 pairs): Insomnia management

Each entry includes:
- `id`: Unique identifier
- `question`: Sample question
- `answer`: Comprehensive answer
- `category`: Health topic category
- `keywords`: Important keywords for matching

## 🤖 How the Chatbot Works

### 1. **Semantic Similarity Matching**
```
User Query → TF-IDF Vectorization → Cosine Similarity Calculation 
→ Best Match Selection → Response with Confidence Score
```

### 2. **Confidence Scoring**
- Similarity scores range from 0 to 1
- Default threshold: 0.3 (30%)
- Scores ≥ 0.3: Provide answer with explanation
- Scores < 0.3: Fallback response

### 3. **Explanation Generation**
Each response includes:
- Similarity score percentage
- Health category
- Matched keywords
- Original question matched
- Matched alternatives

### 4. **Fallback Mechanism**
For low-confidence queries:
```
"I'm not confident about this answer. 
Please consult a qualified medical professional for accurate health advice."
```

## 📈 Key Features

### ✓ TF-IDF Vectorization
- Converts text to numerical vectors
- Handles stemming and stop words
- Uses bigrams for better semantic understanding
- Vocabulary size: ~500 features

### ✓ Cosine Similarity
- Measures angle between query and answer vectors
- Returns values between 0 (no similarity) and 1 (perfect match)
- Geometrically intuitive: closer vectors = higher similarity

### ✓ Automatic Fallback
- Confidence threshold: 0.3
- Prevents giving inappropriate health advice
- Encourages professional consultation

### ✓ Conversation History
- All interactions logged with timestamps
- Includes confidence scores and categories
- JSON format for easy analysis

## 📋 Example Usage

### Python API
```python
from health_chatbot import HealthChatbot

# Initialize chatbot
chatbot = HealthChatbot(
    dataset_path='data/health_qa_dataset.json',
    confidence_threshold=0.3
)

# Ask a question
response = chatbot.answer_query("What are dengue symptoms?")

# Access response data
print(response['answer'])           # The answer
print(response['confidence'])       # Confidence score (0-1)
print(response['explanation'])      # Why this answer was chosen
print(response['category'])         # Health category
```

### Response Structure
```json
{
    "success": true,
    "answer": "Symptoms include sudden high fever...",
    "confidence": 0.75,
    "question_id": 2,
    "category": "dengue",
    "matched_question": "What are the symptoms of dengue?",
    "explanation": "Similarity Score: 75.0%
Category: Dengue...",
    "alternatives": [
        {
            "answer": "...",
            "confidence": 0.45,
            "question": "..."
        }
    ]
}
```

## 📊 Output Files

### 1. `conversation_logs.json`
Logs of all chatbot conversations including:
- Query and response pairs
- Confidence scores
- Health categories
- Timestamps

### 2. `query_response_analysis.json`
Detailed analysis of test queries:
- Query text
- Response snippets
- Confidence percentages
- Success status

### 3. `similarity_scores_analysis.png`
Comprehensive visualization showing:
- Histogram of similarity scores
- Box plot distribution
- Success rate pie chart
- Cumulative distribution
- Category breakdown
- Statistical summary

## 🎯 Performance Metrics

### Success Rate
- Successful matches: High-confidence answers (≥ 0.3)
- Fallback responses: Low-confidence queries (< 0.3)

### Confidence Analysis
- Mean confidence: Typically 60-70% for matched queries
- Distribution: Bimodal (successful matches vs. fallbacks)
- Std deviation: Shows consistency of matching

### Similarity Score Statistics
- Tracked per query
- Helps identify problem areas
- Guides threshold tuning

## 🔬 Example Conversations

### Example 1: Dengue Symptoms
```
USER: What are the symptoms of dengue?
CHATBOT: Symptoms include sudden high fever, severe headache, 
joint and muscle pain, weakness, nausea, and skin rash. 
Symptoms typically appear 4-7 days after infection.
CONFIDENCE: 87%
CATEGORY: Dengue
```

### Example 2: Low Confidence
```
USER: xyz abc random text
CHATBOT: I'm not confident about this answer. 
Please consult a qualified medical professional for accurate health advice.
CONFIDENCE: 15%
RESPONSE TYPE: Fallback
```

## 🛠️ Customization

### Adjust Confidence Threshold
```python
chatbot = HealthChatbot(
    dataset_path='data/health_qa_dataset.json',
    confidence_threshold=0.5  # Higher threshold = stricter matching
)
```

### Add New Q&A Pairs
1. Edit `data/health_qa_dataset.json`
2. Add new entry with id, question, answer, category, keywords
3. Reinitialize chatbot to rebuild TF-IDF model

### Tune TF-IDF Parameters
Edit `health_chatbot.py` `__init__` method:
```python
self.vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words='english',
    max_features=500,      # Adjust vocabulary size
    ngram_range=(1, 2)     # Use unigrams + bigrams
)
```

## 📚 Technical Details

### TF-IDF (Term Frequency-Inverse Document Frequency)
- **TF**: How often a term appears in a document
- **IDF**: How unique a term is across all documents
- **Result**: Words that are frequent but not common are weighted higher

### Cosine Similarity
- Computes: cos(θ) = (A · B) / (||A|| ||B||)
- Range: [0, 1] where 1 = identical, 0 = completely different
- Vectorized for fast computation using scikit-learn

## ⚠️ Important Notes

### Medical Disclaimer
This chatbot is for **educational and informational purposes only**. It is NOT a substitute for professional medical advice. Users should:
- Consult healthcare professionals for medical concerns
- Not rely solely on chatbot responses for diagnosis
- Seek emergency care for serious symptoms

### Limitations
- Restricted to predefined Q&A dataset (50 pairs)
- TF-IDF-based (not deep learning)
- No context preservation between queries
- English language only

## 🚀 Future Improvements

### Potential Enhancements
1. **Sentence-BERT Integration**: Deep learning semantic similarity
2. **Context Awareness**: Multi-turn conversations
3. **Multi-Language**: Support for multiple languages
4. **User Feedback**: Learning from user corrections
5. **Domain Expansion**: More health topics and Q&A pairs
6. **API Deployment**: REST API for web/mobile integration
7. **Chat History**: Persistent storage of conversations

## 📝 License & Attribution

This project is created for educational purposes demonstrating:
- Natural Language Processing (NLP) techniques
- Information Retrieval systems
- Chatbot development
- ML pipeline implementation

## 👨‍💻 Author & Support

**Project**: Health Chatbot System
**Purpose**: Educational demonstration of NLP and Information Retrieval
**Created**: November 2025

For questions or improvements, refer to the source code documentation.

---

**Remember**: Always consult qualified healthcare professionals for medical advice! 🏥
