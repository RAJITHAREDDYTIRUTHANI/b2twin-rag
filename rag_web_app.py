# Enhanced Biosphere 2 Web App with RAG Integration
# Retrieval-Augmented Generation for Superior Sensor Data Analysis

from flask import Flask, render_template_string, request, jsonify
import json
import os
import threading
import time
from rag_database import Biosphere2RAGDatabase
from simple_interface import load_all_sensor_data, create_comprehensive_context

app = Flask(__name__)

# Global variables
sensor_data = {}
context_summary = ""
data_loaded = False
rag_database = None
rag_ready = False

# Enhanced HTML template with RAG features
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biosphere 2 RAG-Powered Sensor Analysis</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .rag-status {
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 20px;
            margin-bottom: 20px;
            text-align: center;
            color: white;
        }
        
        .rag-status.ready {
            background: rgba(76, 175, 80, 0.3);
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .chat-container {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            min-height: 600px;
            display: flex;
            flex-direction: column;
        }
        
        .chat-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .chat-header h2 {
            color: #333;
            font-size: 1.5rem;
        }
        
        .rag-indicator {
            background: linear-gradient(135deg, #4caf50, #45a049);
            color: white;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            max-height: 400px;
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            background: #fafafa;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 15px;
            max-width: 80%;
            word-wrap: break-word;
        }
        
        .message.user {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            margin-left: auto;
            text-align: right;
        }
        
        .message.assistant {
            background: white;
            border: 1px solid #e0e0e0;
            margin-right: auto;
        }
        
        .message.system {
            background: #e8f5e8;
            border: 1px solid #4caf50;
            text-align: center;
            margin: 0 auto;
            font-style: italic;
        }
        
        .message.rag-enhanced {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            border: 1px solid #2196f3;
            position: relative;
        }
        
        .message.rag-enhanced::before {
            content: "🧠 RAG Enhanced";
            position: absolute;
            top: -8px;
            right: 10px;
            background: #2196f3;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.7rem;
        }
        
        .sources {
            margin-top: 10px;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 8px;
            border-left: 3px solid #2196f3;
        }
        
        .sources h4 {
            color: #2196f3;
            margin-bottom: 5px;
            font-size: 0.9rem;
        }
        
        .source-item {
            font-size: 0.8rem;
            color: #666;
            margin-bottom: 3px;
        }
        
        .input-container {
            display: flex;
            gap: 10px;
        }
        
        .question-input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        .question-input:focus {
            border-color: #667eea;
        }
        
        .ask-btn {
            padding: 15px 25px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .ask-btn:hover {
            transform: translateY(-2px);
        }
        
        .ask-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .info-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .info-card h3 {
            color: #333;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .sensor-item {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }
        
        .rag-stats {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .stat-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .stat-label {
            color: #666;
        }
        
        .stat-value {
            color: #333;
            font-weight: bold;
        }
        
        .quick-questions {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .quick-question {
            background: #f8f9fa;
            padding: 10px 15px;
            margin-bottom: 8px;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.2s;
            border: 1px solid #e0e0e0;
        }
        
        .quick-question:hover {
            background: #e9ecef;
        }
        
        .quick-question.rag-enhanced {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            border-color: #2196f3;
        }
        
        .loading {
            display: none;
            text-align: center;
            color: #666;
            font-style: italic;
        }
        
        .loading.show {
            display: block;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-brain"></i> Biosphere 2 RAG-Powered Analysis</h1>
            <p>Advanced AI with Retrieval-Augmented Generation</p>
        </div>
        
        <div class="rag-status" id="ragStatus">
            <i class="fas fa-spinner fa-spin"></i> Initializing RAG Database...
        </div>
        
        <div class="main-content">
            <div class="chat-container">
                <div class="chat-header">
                    <h2><i class="fas fa-comments"></i> Ask Complex Questions</h2>
                    <div class="rag-indicator" id="ragIndicator">
                        <i class="fas fa-brain"></i> RAG Enhanced
                    </div>
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <div class="message system">
                        <i class="fas fa-robot"></i> RAG system initializing... Advanced semantic search capabilities loading.
                    </div>
                </div>
                
                <div class="loading" id="loading">
                    <i class="fas fa-spinner fa-spin"></i> Analyzing with RAG...
                </div>
                
                <div class="input-container">
                    <input type="text" id="questionInput" class="question-input" 
                           placeholder="Ask complex questions about sensor correlations, trends, anomalies..." 
                           onkeypress="handleKeyPress(event)">
                    <button id="askBtn" class="ask-btn" onclick="askQuestion()">
                        <i class="fas fa-paper-plane"></i> Ask
                    </button>
                </div>
            </div>
            
            <div class="sidebar">
                <div class="rag-stats">
                    <h3><i class="fas fa-chart-bar"></i> RAG Database Stats</h3>
                    <div id="ragStats">
                        <div class="stat-item">
                            <span class="stat-label">Documents:</span>
                            <span class="stat-value" id="docCount">-</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Embeddings:</span>
                            <span class="stat-value" id="embeddingCount">-</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Vector Index:</span>
                            <span class="stat-value" id="vectorIndexSize">-</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Status:</span>
                            <span class="stat-value" id="ragStatusText">Loading...</span>
                        </div>
                    </div>
                </div>
                
                <div class="info-card">
                    <h3><i class="fas fa-chart-line"></i> Sensor Overview</h3>
                    {% for sensor_type, data in sensor_data.items() %}
                    <div class="sensor-item">
                        <h4>{{ sensor_type.replace('_', ' ').title() }}</h4>
                        <p><strong>Readings:</strong> {{ data.total_readings }}</p>
                        <p><strong>Period:</strong> {{ data.time_range }}</p>
                        {% if data.value_stats %}
                        <p><strong>Range:</strong> {{ "%.1f"|format(data.value_stats.min) }}°F - {{ "%.1f"|format(data.value_stats.max) }}°F</p>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
                
                <div class="quick-questions">
                    <h3><i class="fas fa-lightning-bolt"></i> Advanced Questions</h3>
                    <div class="quick-question rag-enhanced" onclick="askQuickQuestion('What are the correlations between temperature and fan operations?')">
                        What are the correlations between temperature and fan operations?
                    </div>
                    <div class="quick-question rag-enhanced" onclick="askQuickQuestion('Identify any anomalies or unusual patterns in the sensor data')">
                        Identify any anomalies or unusual patterns
                    </div>
                    <div class="quick-question rag-enhanced" onclick="askQuickQuestion('What is the overall system health based on all sensor readings?')">
                        What is the overall system health?
                    </div>
                    <div class="quick-question rag-enhanced" onclick="askQuickQuestion('How do valve operations correlate with environmental conditions?')">
                        How do valve operations correlate with environmental conditions?
                    </div>
                    <div class="quick-question rag-enhanced" onclick="askQuickQuestion('What trends can you identify across the monitoring period?')">
                        What trends can you identify across the monitoring period?
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                askQuestion();
            }
        }
        
        function askQuickQuestion(question) {
            document.getElementById('questionInput').value = question;
            askQuestion();
        }
        
        function askQuestion() {
            const input = document.getElementById('questionInput');
            const question = input.value.trim();
            
            if (!question) return;
            
            addMessage(question, 'user');
            input.value = '';
            showLoading(true);
            
            fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({question: question})
            })
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                if (data.sources && data.sources.length > 0) {
                    addRAGMessage(data.answer, data.sources);
                } else {
                    addMessage(data.answer, 'assistant');
                }
            })
            .catch(error => {
                showLoading(false);
                addMessage('Sorry, there was an error processing your question.', 'assistant');
            });
        }
        
        function addMessage(text, type) {
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            messageDiv.textContent = text;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        function addRAGMessage(text, sources) {
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message assistant rag-enhanced';
            
            const contentDiv = document.createElement('div');
            contentDiv.textContent = text;
            messageDiv.appendChild(contentDiv);
            
            if (sources && sources.length > 0) {
                const sourcesDiv = document.createElement('div');
                sourcesDiv.className = 'sources';
                
                const sourcesTitle = document.createElement('h4');
                sourcesTitle.textContent = 'Sources:';
                sourcesDiv.appendChild(sourcesTitle);
                
                sources.forEach(source => {
                    const sourceItem = document.createElement('div');
                    sourceItem.className = 'source-item';
                    sourceItem.textContent = `${source.doc_id} (${source.similarity_score.toFixed(3)})`;
                    sourcesDiv.appendChild(sourceItem);
                });
                
                messageDiv.appendChild(sourcesDiv);
            }
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        function showLoading(show) {
            const loading = document.getElementById('loading');
            const askBtn = document.getElementById('askBtn');
            
            if (show) {
                loading.classList.add('show');
                askBtn.disabled = true;
            } else {
                loading.classList.remove('show');
                askBtn.disabled = false;
            }
        }
        
        function updateRAGStats() {
            fetch('/api/rag-stats')
            .then(response => response.json())
            .then(data => {
                document.getElementById('docCount').textContent = data.documents;
                document.getElementById('embeddingCount').textContent = data.embeddings;
                document.getElementById('vectorIndexSize').textContent = data.vector_index_size;
                document.getElementById('ragStatusText').textContent = data.status;
                
                if (data.status === 'ready') {
                    document.getElementById('ragStatus').innerHTML = '<i class="fas fa-check-circle"></i> RAG Database Ready';
                    document.getElementById('ragStatus').classList.add('ready');
                }
            })
            .catch(error => {
                console.error('Error fetching RAG stats:', error);
            });
        }
        
        // Update RAG stats every 2 seconds
        setInterval(updateRAGStats, 2000);
        
        // Initial focus
        document.getElementById('questionInput').focus();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, sensor_data=sensor_data)

@app.route('/ask', methods=['POST'])
def ask_question_endpoint():
    global context_summary, rag_database
    
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'answer': 'Please enter a question.'})
        
        # Use RAG if available, otherwise fallback to simple context
        if rag_ready and rag_database:
            # Get RAG-enhanced context
            rag_context = rag_database.get_context_for_question(question)
            
            # Search for relevant sources
            sources = rag_database.search(question, top_k=3)
            
            # Enhanced prompt with RAG context
            prompt = f"""
            You are a Biosphere 2 environmental analyst with access to advanced RAG (Retrieval-Augmented Generation) capabilities.
            
            RELEVANT CONTEXT FROM RAG DATABASE:
            {rag_context}
            
            USER QUESTION: {question}
            
            RULES:
            - Answer in 1-2 sentences maximum
            - Use specific numbers from the RAG context
            - Be direct and actionable
            - If data is missing, say "No [specific data] available"
            - Focus on what the RAG context shows
            """
            
            # Get answer from Claude with RAG context
            from simple_interface import client
            response = client.messages.create(
                model="claude-3-5-sonnet",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            answer = response.content[0].text
            
            return jsonify({
                'answer': answer,
                'sources': sources
            })
        else:
            # Fallback to simple context
            from simple_interface import ask_question
            answer = ask_question(question, context_summary)
            return jsonify({'answer': answer})
        
    except Exception as e:
        return jsonify({'answer': f'Error processing question: {str(e)}'})

@app.route('/api/rag-stats')
def get_rag_stats():
    global rag_database, rag_ready
    
    if rag_database and rag_ready:
        stats = rag_database.get_database_stats()
        stats['status'] = 'ready'
        return jsonify(stats)
    else:
        return jsonify({
            'documents': 0,
            'embeddings': 0,
            'vector_index_size': 0,
            'status': 'loading'
        })

@app.route('/api/data')
def get_sensor_data():
    return jsonify(sensor_data)

def load_data_background():
    global sensor_data, context_summary, data_loaded, rag_database, rag_ready
    
    print("Loading Biosphere 2 sensor data...")
    sensor_data = load_all_sensor_data()
    context_summary = create_comprehensive_context(sensor_data)
    data_loaded = True
    print("[SUCCESS] Sensor data loaded!")
    
    # Initialize RAG database
    print("Initializing RAG database...")
    try:
        rag_database = Biosphere2RAGDatabase()
        
        # Create document chunks
        print("Creating document chunks...")
        chunks = rag_database.create_document_chunks(sensor_data)
        
        # Add documents to database
        print("Adding documents to RAG database...")
        rag_database.add_documents(chunks)
        
        # Build vector index
        print("Building vector index...")
        rag_database.build_vector_index()
        
        rag_ready = True
        print("[SUCCESS] RAG database ready!")
        
    except Exception as e:
        print(f"[WARNING] RAG database initialization failed: {e}")
        print("Falling back to simple context mode...")
        rag_ready = False

if __name__ == "__main__":
    # Load data in background thread
    data_thread = threading.Thread(target=load_data_background)
    data_thread.daemon = True
    data_thread.start()
    
    print("Starting Biosphere 2 RAG-Powered Web Interface...")
    print("Loading sensor data and initializing RAG database...")
    print("Web interface will be available at: http://localhost:5000")
    print("Advanced semantic search capabilities loading...")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

