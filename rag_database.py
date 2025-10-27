# Biosphere 2 RAG Database Implementation
# Retrieval-Augmented Generation for Enhanced Sensor Data Analysis

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Tuple
import sqlite3
from pathlib import Path

# For embeddings and vector operations
try:
    import openai
    from sentence_transformers import SentenceTransformer
    import faiss
    HAS_EMBEDDINGS = True
except ImportError:
    HAS_EMBEDDINGS = False
    print("Install required packages: pip install openai sentence-transformers faiss-cpu")

class Biosphere2RAGDatabase:
    """
    RAG Database for Biosphere 2 Sensor Data Analysis
    
    Features:
    - Vector embeddings of sensor data
    - Semantic search capabilities
    - Context-aware retrieval
    - Multi-modal data integration
    """
    
    def __init__(self, db_path: str = "biosphere2_rag.db", embedding_model: str = "all-MiniLM-L6-v2"):
        self.db_path = db_path
        self.embedding_model_name = embedding_model
        self.embedding_model = None
        self.vector_index = None
        self.documents = []
        self.metadata = []
        
        # Initialize database
        self.init_database()
        
        # Load embedding model if available
        if HAS_EMBEDDINGS:
            self.load_embedding_model()
    
    def init_database(self):
        """Initialize SQLite database for metadata storage"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id TEXT UNIQUE,
                content TEXT,
                metadata TEXT,
                embedding_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_type TEXT,
                timestamp TEXT,
                value REAL,
                status TEXT,
                metadata TEXT,
                doc_id TEXT,
                FOREIGN KEY (doc_id) REFERENCES documents (doc_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id TEXT,
                embedding_vector BLOB,
                FOREIGN KEY (doc_id) REFERENCES documents (doc_id)
            )
        ''')
        
        self.conn.commit()
        print(f"[SUCCESS] RAG Database initialized: {self.db_path}")
    
    def load_embedding_model(self):
        """Load sentence transformer model for embeddings"""
        try:
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            print(f"[SUCCESS] Embedding model loaded: {self.embedding_model_name}")
        except Exception as e:
            print(f"[ERROR] Error loading embedding model: {e}")
            self.embedding_model = None
    
    def create_document_chunks(self, sensor_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create document chunks from sensor data for RAG processing
        
        Args:
            sensor_data: Dictionary containing sensor data
            
        Returns:
            List of document chunks with metadata
        """
        chunks = []
        
        for sensor_type, data in sensor_data.items():
            # Create different types of chunks for each sensor
            
            # 1. Summary chunk
            summary_chunk = {
                "doc_id": f"{sensor_type}_summary",
                "content": f"""
                {sensor_type.replace('_', ' ').title()} Sensor Summary:
                - Total readings: {data.get('total_readings', 0)}
                - Time range: {data.get('time_range', 'Unknown')}
                - Value range: {data.get('value_stats', {}).get('min', 'N/A')} to {data.get('value_stats', {}).get('max', 'N/A')}
                - Sensor type: {sensor_type}
                """,
                "metadata": {
                    "sensor_type": sensor_type,
                    "chunk_type": "summary",
                    "total_readings": data.get('total_readings', 0),
                    "time_range": data.get('time_range', 'Unknown')
                }
            }
            chunks.append(summary_chunk)
            
            # 2. Sample data chunks
            if 'sample_data' in data and data['sample_data']:
                for i, sample in enumerate(data['sample_data'][:5]):  # First 5 samples
                    sample_chunk = {
                        "doc_id": f"{sensor_type}_sample_{i}",
                        "content": f"""
                        {sensor_type.replace('_', ' ').title()} Sample Data {i+1}:
                        - Timestamp: {sample.get(' TIMESTAMP', 'Unknown')}
                        - Value: {sample.get(' VALUE', 'N/A')}
                        - Status: {sample.get(' STATUS_TAG', 'Unknown')}
                        - ID: {sample.get('ID', 'Unknown')}
                        """,
                        "metadata": {
                            "sensor_type": sensor_type,
                            "chunk_type": "sample_data",
                            "sample_index": i,
                            "timestamp": sample.get(' TIMESTAMP', 'Unknown'),
                            "value": sample.get(' VALUE', None)
                        }
                    }
                    chunks.append(sample_chunk)
            
            # 3. Statistical analysis chunk
            if 'value_stats' in data:
                stats_chunk = {
                    "doc_id": f"{sensor_type}_statistics",
                    "content": f"""
                    {sensor_type.replace('_', ' ').title()} Statistical Analysis:
                    - Minimum value: {data['value_stats'].get('min', 'N/A')}
                    - Maximum value: {data['value_stats'].get('max', 'N/A')}
                    - Average value: {data['value_stats'].get('mean', 'N/A')}
                    - Data quality: {'Good' if data.get('total_readings', 0) > 100 else 'Limited'}
                    """,
                    "metadata": {
                        "sensor_type": sensor_type,
                        "chunk_type": "statistics",
                        "min_value": data['value_stats'].get('min'),
                        "max_value": data['value_stats'].get('max'),
                        "mean_value": data['value_stats'].get('mean')
                    }
                }
                chunks.append(stats_chunk)
        
        # 4. System overview chunk
        total_readings = sum(data.get('total_readings', 0) for data in sensor_data.values())
        system_chunk = {
            "doc_id": "system_overview",
            "content": f"""
            Biosphere 2 Environmental Monitoring System Overview:
            - Total sensors: {len(sensor_data)}
            - Total readings: {total_readings}
            - Monitoring period: September 21-28, 2025
            - System status: Operational
            - Data quality: Comprehensive
            """,
            "metadata": {
                "sensor_type": "system",
                "chunk_type": "overview",
                "total_sensors": len(sensor_data),
                "total_readings": total_readings
            }
        }
        chunks.append(system_chunk)
        
        return chunks
    
    def add_documents(self, chunks: List[Dict[str, Any]]):
        """Add document chunks to the database"""
        cursor = self.conn.cursor()
        
        for chunk in chunks:
            try:
                # Insert document
                cursor.execute('''
                    INSERT OR REPLACE INTO documents (doc_id, content, metadata)
                    VALUES (?, ?, ?)
                ''', (
                    chunk['doc_id'],
                    chunk['content'],
                    json.dumps(chunk['metadata'])
                ))
                
                # Generate embedding if model is available
                if self.embedding_model:
                    embedding = self.embedding_model.encode(chunk['content'])
                    
                    # Store embedding
                    cursor.execute('''
                        INSERT OR REPLACE INTO embeddings (doc_id, embedding_vector)
                        VALUES (?, ?)
                    ''', (
                        chunk['doc_id'],
                        embedding.tobytes()
                    ))
                
                self.documents.append(chunk)
                
            except Exception as e:
                print(f"[ERROR] Error adding document {chunk['doc_id']}: {e}")
        
        self.conn.commit()
        print(f"[SUCCESS] Added {len(chunks)} documents to RAG database")
    
    def build_vector_index(self):
        """Build FAISS vector index for similarity search"""
        if not self.embedding_model:
            print("[ERROR] No embedding model available")
            return
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT doc_id, embedding_vector FROM embeddings')
        results = cursor.fetchall()
        
        if not results:
            print("[ERROR] No embeddings found")
            return
        
        # Extract embeddings
        embeddings = []
        doc_ids = []
        
        for doc_id, embedding_bytes in results:
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
            embeddings.append(embedding)
            doc_ids.append(doc_id)
        
        # Build FAISS index
        embeddings_array = np.array(embeddings)
        dimension = embeddings_array.shape[1]
        
        self.vector_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.vector_index.add(embeddings_array)
        
        # Store doc_ids for retrieval
        self.doc_ids = doc_ids
        
        print(f"[SUCCESS] Vector index built with {len(embeddings)} embeddings")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant documents using semantic similarity
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of relevant documents with similarity scores
        """
        if not self.vector_index or not self.embedding_model:
            print("[ERROR] Vector index or embedding model not available")
            return []
        
        # Encode query
        query_embedding = self.embedding_model.encode([query])
        
        # Search
        scores, indices = self.vector_index.search(query_embedding, top_k)
        
        # Retrieve documents
        results = []
        cursor = self.conn.cursor()
        
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.doc_ids):
                doc_id = self.doc_ids[idx]
                
                cursor.execute('''
                    SELECT content, metadata FROM documents WHERE doc_id = ?
                ''', (doc_id,))
                
                result = cursor.fetchone()
                if result:
                    content, metadata_json = result
                    metadata = json.loads(metadata_json)
                    
                    results.append({
                        'doc_id': doc_id,
                        'content': content,
                        'metadata': metadata,
                        'similarity_score': float(score)
                    })
        
        return results
    
    def get_context_for_question(self, question: str, max_context_length: int = 2000) -> str:
        """
        Get relevant context for a question using RAG
        
        Args:
            question: User question
            max_context_length: Maximum context length in characters
            
        Returns:
            Relevant context string
        """
        # Search for relevant documents
        search_results = self.search(question, top_k=5)
        
        # Build context
        context_parts = []
        current_length = 0
        
        for result in search_results:
            if current_length + len(result['content']) <= max_context_length:
                context_parts.append(f"[{result['metadata'].get('sensor_type', 'unknown')}] {result['content']}")
                current_length += len(result['content'])
            else:
                break
        
        return "\n\n".join(context_parts)
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        cursor = self.conn.cursor()
        
        # Count documents
        cursor.execute('SELECT COUNT(*) FROM documents')
        doc_count = cursor.fetchone()[0]
        
        # Count embeddings
        cursor.execute('SELECT COUNT(*) FROM embeddings')
        embedding_count = cursor.fetchone()[0]
        
        # Count sensor readings
        cursor.execute('SELECT COUNT(*) FROM sensor_readings')
        reading_count = cursor.fetchone()[0]
        
        return {
            'documents': doc_count,
            'embeddings': embedding_count,
            'sensor_readings': reading_count,
            'vector_index_size': len(self.doc_ids) if hasattr(self, 'doc_ids') else 0
        }

# Example usage and testing
if __name__ == "__main__":
    print("[RAG INIT] Initializing Biosphere 2 RAG Database...")
    
    # Initialize RAG database
    rag_db = Biosphere2RAGDatabase()
    
    # Load sensor data (you would load your actual data here)
    from simple_interface import load_all_sensor_data, create_comprehensive_context
    
    print("[DATA LOAD] Loading sensor data...")
    sensor_data = load_all_sensor_data()
    
    print("[CHUNKS] Creating document chunks...")
    chunks = rag_db.create_document_chunks(sensor_data)
    
    print("[DOCS] Adding documents to database...")
    rag_db.add_documents(chunks)
    
    print("[INDEX] Building vector index...")
    rag_db.build_vector_index()
    
    print("[STATS] Database statistics:")
    stats = rag_db.get_database_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n[SEARCH] Testing RAG search...")
    test_queries = [
        "What is the temperature range?",
        "How many fan readings were recorded?",
        "What are the valve system statuses?",
        "Tell me about the monitoring period"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = rag_db.search(query, top_k=3)
        for i, result in enumerate(results):
            print(f"  {i+1}. {result['doc_id']} (score: {result['similarity_score']:.3f})")
            print(f"     {result['content'][:100]}...")
    
    print("\n[SUCCESS] RAG Database setup complete!")

