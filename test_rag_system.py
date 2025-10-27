# Biosphere 2 RAG System Test Suite
# Tests the RAG database functionality

import os
import sys
import json
from datetime import datetime

def test_rag_system():
    """Test the RAG database system"""
    
    print("Testing Biosphere 2 RAG Database...")
    
    try:
        # Test imports
        print("Testing imports...")
        from rag_database import Biosphere2RAGDatabase
        from simple_interface import load_all_sensor_data, create_comprehensive_context
        print("All imports successful")
        
        # Test data loading
        print("\nTesting data loading...")
        sensor_data = load_all_sensor_data()
        print(f"Loaded {len(sensor_data)} sensor types")
        
        # Test RAG database initialization
        print("\nTesting RAG database initialization...")
        rag_db = Biosphere2RAGDatabase()
        print("RAG database initialized")
        
        # Test document chunking
        print("\nTesting document chunking...")
        chunks = rag_db.create_document_chunks(sensor_data)
        print(f"Created {len(chunks)} document chunks")
        
        # Test document addition
        print("\nTesting document addition...")
        rag_db.add_documents(chunks)
        print("Documents added to database")
        
        # Test vector index building
        print("\nTesting vector index building...")
        rag_db.build_vector_index()
        print("Vector index built")
        
        # Test search functionality
        print("\nTesting search functionality...")
        
        test_queries = [
            "What is the temperature range?",
            "How many fan readings are there?",
            "What sensors monitor humidity?",
            "Show me valve position data"
        ]
        
        for query in test_queries:
            results = rag_db.search(query, top_k=3)
            print(f"Query: '{query}' -> Found {len(results)} results")
            if results:
                print(f"  Top result: {results[0]['content'][:100]}...")
        
        # Test context generation
        print("\nTesting context generation...")
        context = rag_db.search("temperature sensor data", top_k=5)
        context_text = "\n".join([r['content'] for r in context])
        print(f"Generated context ({len(context_text)} characters)")
        
        # Test database statistics
        print("\nTesting database statistics...")
        stats = rag_db.get_database_stats()
        print(f"Database stats: {stats}")
        
        print("\nAll RAG tests passed successfully!")
        return True
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all dependencies are installed: pip install sentence-transformers faiss-cpu")
        return False
    except Exception as e:
        print(f"Test failed: {e}")
        return False

def test_web_app():
    """Test the RAG web application"""
    
    print("\nTesting RAG Web App...")
    
    try:
        import requests
        import time
        
        # Check if web app is running
        try:
            response = requests.get("http://localhost:5000", timeout=5)
            if response.status_code == 200:
                print("Web app is running")
            else:
                print("Web app returned non-200 status")
                return False
        except requests.exceptions.ConnectionError:
            print("Please start the web app manually: python rag_web_app.py")
            return False
        
        # Test RAG stats endpoint
        try:
            response = requests.get("http://localhost:5000/api/rag-stats", timeout=10)
            if response.status_code == 200:
                stats = response.json()
                print(f"RAG stats API working: {stats}")
            else:
                print(f"RAG stats API failed: {response.status_code}")
        except Exception as e:
            print(f"RAG stats API error: {e}")
        
        # Test question endpoint
        try:
            test_question = {"question": "What is the temperature range in the data?"}
            response = requests.post("http://localhost:5000/api/ask", 
                                   json=test_question, timeout=15)
            if response.status_code == 200:
                result = response.json()
                print(f"Question API working: {result['answer'][:100]}...")
                if 'sources' in result:
                    print(f"RAG sources found: {len(result['sources'])} sources")
            else:
                print(f"Question API failed: {response.status_code}")
        except Exception as e:
            print(f"Question API error: {e}")
        
        return True
        
    except Exception as e:
        print(f"Web app test failed: {e}")
        return False

if __name__ == "__main__":
    print("Biosphere 2 RAG System Test Suite")
    print("=" * 50)
    
    # Test RAG database
    rag_success = test_rag_system()
    
    # Test web app (optional)
    web_success = test_web_app()
    
    # Summary
    print("\n" + "=" * 50)
    if rag_success:
        if web_success:
            print("\nAll tests passed! RAG system is ready for deployment.")
        else:
            print("\nRAG database works, but web app needs attention.")
    else:
        print("\nRAG database tests failed. Please fix issues before proceeding.")
    
    print("\nNext steps:")
    print("1. Run: python rag_web_app.py")
    print("2. Open: http://localhost:5000")
    print("3. Test the RAG-powered chat interface")
    print("4. Deploy to production when ready")