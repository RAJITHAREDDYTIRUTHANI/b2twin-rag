# Biosphere 2 AI RAG System

An intelligent RAG (Retrieval-Augmented Generation) system for querying Biosphere 2 sensor data using Claude AI.

## Features

- **RAG-powered Q&A**: Ask natural language questions about your sensor data
- **Semantic Search**: 384-dimensional embeddings for intelligent document retrieval
- **Web Interface**: Interactive UI for real-time queries
- **Multi-Sensor Support**: Temperature, fan control, valve operations, and more

## Project Structure

```
├── data/                    # Sensor data CSV files
├── results/                 # Analysis results
├── rag_database.py         # RAG system core
├── rag_web_app.py          # Flask web application
├── requirements_rag.txt    # Dependencies
└── README.md              # This file
```

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements_rag.txt
```

## Usage

### Run the RAG Web Application

```bash
python spectacular_rag_web_app.py
```

Then open your browser to: `http://localhost:5000`

### Available Endpoints

- `GET /` - Web interface
- `POST /api/query` - Query the RAG system
- `GET /api/rag-stats` - System statistics

## How It Works

1. **Document Creation**: Sensor data is chunked into searchable documents
2. **Embedding Generation**: Each document becomes a 384-dimensional vector using SentenceTransformer
3. **Vector Index**: FAISS index enables fast semantic search
4. **Query Processing**: Questions are converted to vectors and matched against documents
5. **Context Retrieval**: Most relevant documents retrieved based on similarity
6. **AI Response**: Claude AI generates intelligent answers using retrieved context

## Technical Stack

- **Language**: Python 3.8+
- **Web Framework**: Flask
- **AI Model**: Claude (Anthropic API)
- **Embeddings**: SentenceTransformer (all-MiniLM-L6-v2)
- **Vector Database**: FAISS
- **Metadata Storage**: SQLite

## API Usage

### Query Example

```python
POST /api/query
{
    "question": "What is the temperature range?"
}

Response:
{
    "answer": "Based on your sensor data...",
    "sources": ["temperature_summary"],
    "similarity_score": 0.95
}
```

## Configuration

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY=your_key_here
```

Or create a `.env` file:

```
ANTHROPIC_API_KEY=your_key_here
```

## License

This project is for educational and research purposes related to Biosphere 2 data analysis.