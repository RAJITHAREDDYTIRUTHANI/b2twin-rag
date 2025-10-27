# Enhanced Biosphere 2 RAG Web App with Modern UI
# Advanced Retrieval-Augmented Generation Interface

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

# Enhanced Modern HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biosphere 2 RAG-Powered Sensor Analysis</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #2d3748;
            line-height: 1.6;
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
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
            font-weight: 300;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .chat-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }
        
        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .card h3 {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 16px;
            color: #2d3748;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .chat-container {
            height: 500px;
            overflow-y: auto;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            background: #f8fafc;
        }
        
        .message {
            margin-bottom: 20px;
            animation: fadeInUp 0.3s ease-out;
        }
        
        .message.user {
            text-align: right;
        }
        
        .message.assistant {
            text-align: left;
        }
        
        .message-content {
            display: inline-block;
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .message.assistant .message-content {
            background: white;
            border: 1px solid #e2e8f0;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .message-time {
            font-size: 0.75rem;
            color: #718096;
            margin-top: 4px;
        }
        
        .input-container {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .message-input {
            flex: 1;
            padding: 16px 20px;
            border: 2px solid #e2e8f0;
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
            background: white;
        }
        
        .message-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .send-button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
        }
        
        .send-button:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }
        
        .send-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .quick-questions {
            display: grid;
            gap: 8px;
        }
        
        .quick-question {
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 12px 16px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.9rem;
            color: #4a5568;
        }
        
        .quick-question:hover {
            background: #edf2f7;
            border-color: #667eea;
            transform: translateY(-1px);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        
        .stat-item {
            text-align: center;
            padding: 16px;
            background: #f7fafc;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 4px;
        }
        
        .stat-label {
            font-size: 0.8rem;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .status-ready {
            background: #c6f6d5;
            color: #22543d;
        }
        
        .status-loading {
            background: #fef5e7;
            color: #744210;
        }
        
        .status-error {
            background: #fed7d7;
            color: #742a2a;
        }
        
        .loading-spinner {
            width: 16px;
            height: 16px;
            border: 2px solid #e2e8f0;
            border-top: 2px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        .sources-section {
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid #e2e8f0;
        }
        
        .sources-title {
            font-size: 0.85rem;
            font-weight: 600;
            color: #4a5568;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .source-item {
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 8px 12px;
            margin-bottom: 6px;
            font-size: 0.8rem;
            color: #4a5568;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .typing-indicator {
            display: none;
            padding: 12px 16px;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            border-bottom-left-radius: 4px;
            margin-bottom: 20px;
            max-width: 80px;
        }
        
        .typing-dots {
            display: flex;
            gap: 4px;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            background: #a0aec0;
            border-radius: 50%;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes typing {
            0%, 80%, 100% {
                transform: scale(0.8);
                opacity: 0.5;
            }
            40% {
                transform: scale(1);
                opacity: 1;
            }
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .chat-container {
                height: 400px;
            }
            
            .message-content {
                max-width: 90%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-seedling"></i> Biosphere 2 RAG Analysis</h1>
            <p>Advanced AI-Powered Sensor Data Intelligence</p>
        </div>
        
        <div class="main-content">
            <div class="chat-section">
                <div class="chat-container" id="chatContainer">
                    <div class="message assistant">
                        <div class="message-content">
                            Welcome to Biosphere 2 RAG Analysis! I'm your AI assistant powered by advanced retrieval-augmented generation. I can help you analyze sensor data, answer questions about environmental conditions, and provide insights about the Biosphere 2 facility.
                            <br><br>
                            <strong>What I can help with:</strong>
                            <ul style="margin: 8px 0; padding-left: 20px;">
                                <li>Temperature and humidity analysis</li>
                                <li>Fan and valve system status</li>
                                <li>Environmental monitoring insights</li>
                                <li>Data trends and patterns</li>
                                <li>System performance metrics</li>
                            </ul>
                            Ask me anything about your sensor data!
                        </div>
                        <div class="message-time" id="welcomeTime"></div>
                    </div>
                    
                    <div class="typing-indicator" id="typingIndicator">
                        <div class="typing-dots">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                    </div>
                </div>
                
                <div class="input-container">
                    <input type="text" class="message-input" id="messageInput" placeholder="Ask about your sensor data..." autocomplete="off">
                    <button class="send-button" id="sendButton" onclick="sendMessage()">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
            </div>
            
            <div class="sidebar">
                <div class="card">
                    <h3><i class="fas fa-bolt"></i> System Status</h3>
                    <div class="status-indicator" id="systemStatus">
                        <div class="loading-spinner"></div>
                        <span>Initializing...</span>
                    </div>
                </div>
                
                <div class="card">
                    <h3><i class="fas fa-chart-bar"></i> RAG Statistics</h3>
                    <div class="stats-grid" id="ragStats">
                        <div class="stat-item">
                            <div class="stat-value">-</div>
                            <div class="stat-label">Documents</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">-</div>
                            <div class="stat-label">Embeddings</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">-</div>
                            <div class="stat-label">Sensors</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">-</div>
                            <div class="stat-label">Readings</div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h3><i class="fas fa-lightbulb"></i> Quick Questions</h3>
                    <div class="quick-questions">
                        <div class="quick-question" onclick="askQuickQuestion('What is the temperature range?')">
                            Temperature range?
                        </div>
                        <div class="quick-question" onclick="askQuickQuestion('How many fan readings are there?')">
                            Fan readings count?
                        </div>
                        <div class="quick-question" onclick="askQuickQuestion('What are the valve system statuses?')">
                            Valve statuses?
                        </div>
                        <div class="quick-question" onclick="askQuickQuestion('Show me the monitoring period')">
                            Monitoring period?
                        </div>
                        <div class="quick-question" onclick="askQuickQuestion('What sensors are available?')">
                            Available sensors?
                        </div>
                        <div class="quick-question" onclick="askQuickQuestion('Give me a data summary')">
                            Data summary?
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let isProcessing = false;
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('welcomeTime').textContent = new Date().toLocaleTimeString();
            updateSystemStatus();
            updateRAGStats();
            
            // Auto-refresh stats every 10 seconds
            setInterval(updateRAGStats, 10000);
            
            // Enter key to send message
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !isProcessing) {
                    sendMessage();
                }
            });
        });
        
        function updateSystemStatus() {
            fetch('/api/system-status')
                .then(response => response.json())
                .then(data => {
                    const statusEl = document.getElementById('systemStatus');
                    if (data.rag_ready && data.data_loaded) {
                        statusEl.className = 'status-indicator status-ready';
                        statusEl.innerHTML = '<i class="fas fa-check-circle"></i><span>System Ready</span>';
                    } else if (data.data_loaded) {
                        statusEl.className = 'status-indicator status-loading';
                        statusEl.innerHTML = '<div class="loading-spinner"></div><span>Building RAG...</span>';
                    } else {
                        statusEl.className = 'status-indicator status-loading';
                        statusEl.innerHTML = '<div class="loading-spinner"></div><span>Loading Data...</span>';
                    }
                })
                .catch(error => {
                    const statusEl = document.getElementById('systemStatus');
                    statusEl.className = 'status-indicator status-error';
                    statusEl.innerHTML = '<i class="fas fa-exclamation-triangle"></i><span>Error</span>';
                });
        }
        
        function updateRAGStats() {
            fetch('/api/rag-stats')
                .then(response => response.json())
                .then(data => {
                    const statsEl = document.getElementById('ragStats');
                    const statItems = statsEl.querySelectorAll('.stat-value');
                    if (statItems.length >= 4) {
                        statItems[0].textContent = data.documents || 0;
                        statItems[1].textContent = data.embeddings || 0;
                        statItems[2].textContent = data.sensor_types || 0;
                        statItems[3].textContent = data.total_readings || 0;
                    }
                })
                .catch(error => console.log('Stats update failed:', error));
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message || isProcessing) return;
            
            // Add user message
            addMessage(message, 'user');
            input.value = '';
            
            // Show typing indicator
            showTypingIndicator();
            
            // Send to server
            isProcessing = true;
            document.getElementById('sendButton').disabled = true;
            
            fetch('/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: message })
            })
            .then(response => response.json())
            .then(data => {
                hideTypingIndicator();
                addMessage(data.answer, 'assistant', data.sources);
            })
            .catch(error => {
                hideTypingIndicator();
                addMessage('Sorry, I encountered an error processing your request. Please try again.', 'assistant');
                console.error('Error:', error);
            })
            .finally(() => {
                isProcessing = false;
                document.getElementById('sendButton').disabled = false;
                input.focus();
            });
        }
        
        function askQuickQuestion(question) {
            document.getElementById('messageInput').value = question;
            sendMessage();
        }
        
        function addMessage(content, sender, sources = null) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            let messageHTML = `<div class="message-content">${content}</div>`;
            
            if (sources && sources.length > 0) {
                messageHTML += `
                    <div class="sources-section">
                        <div class="sources-title">
                            <i class="fas fa-link"></i>
                            Sources (${sources.length})
                        </div>
                        ${sources.map(source => `
                            <div class="source-item">
                                ${source.doc_id}: ${source.content.substring(0, 100)}...
                            </div>
                        `).join('')}
                    </div>
                `;
            }
            
            messageHTML += `<div class="message-time">${new Date().toLocaleTimeString()}</div>`;
            
            messageDiv.innerHTML = messageHTML;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function showTypingIndicator() {
            document.getElementById('typingIndicator').style.display = 'block';
            document.getElementById('chatContainer').scrollTop = document.getElementById('chatContainer').scrollHeight;
        }
        
        function hideTypingIndicator() {
            document.getElementById('typingIndicator').style.display = 'none';
        }
    </script>
</body>
</html>
"""

def load_data_background():
    """Load sensor data and initialize RAG database in background"""
    global sensor_data, context_summary, data_loaded, rag_database, rag_ready
    
    try:
        print("Loading Biosphere 2 sensor data...")
        sensor_data = load_all_sensor_data()
        context_summary = create_comprehensive_context(sensor_data)
        data_loaded = True
        print("[SUCCESS] Sensor data loaded!")
        
        print("Initializing RAG database...")
        rag_database = Biosphere2RAGDatabase()
        
        print("Creating document chunks...")
        chunks = rag_database.create_document_chunks(sensor_data)
        
        print("Adding documents to RAG database...")
        rag_database.add_documents(chunks)
        
        print("Building vector index...")
        rag_database.build_vector_index()
        
        rag_ready = True
        print("[SUCCESS] RAG database ready!")
        
    except Exception as e:
        print(f"[ERROR] Failed to initialize RAG system: {e}")
        rag_ready = False

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/system-status')
def get_system_status():
    """Get system status"""
    return jsonify({
        'data_loaded': data_loaded,
        'rag_ready': rag_ready,
        'sensor_count': len(sensor_data) if sensor_data else 0
    })

@app.route('/api/rag-stats')
def get_rag_stats():
    """Get RAG database statistics"""
    try:
        if rag_database:
            stats = rag_database.get_database_stats()
            return jsonify(stats)
        else:
            return jsonify({
                'documents': 0,
                'embeddings': 0,
                'sensor_types': 0,
                'total_readings': 0
            })
    except Exception as e:
        print(f"[ERROR] Failed to get RAG stats: {e}")
        return jsonify({
            'documents': 0,
            'embeddings': 0,
            'sensor_types': 0,
            'total_readings': 0
        })

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Ask a question using RAG system"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'answer': 'Please provide a question.', 'sources': []})
        
        if not rag_ready or not rag_database:
            return jsonify({
                'answer': 'RAG system is still initializing. Please wait a moment and try again.',
                'sources': []
            })
        
        # Use RAG system to answer
        if hasattr(rag_database, 'answer_with_rag'):
            answer, sources = rag_database.answer_with_rag(question)
        else:
            # Fallback to basic search
            search_results = rag_database.search(question, top_k=3)
            sources = search_results
            
            # Simple answer generation (you could enhance this with Claude API)
            if search_results:
                answer = f"Based on the sensor data, I found {len(search_results)} relevant sources. "
                answer += f"The top result shows: {search_results[0]['content'][:200]}..."
            else:
                answer = "I couldn't find specific information about that in the sensor data."
        
        return jsonify({
            'answer': answer,
            'sources': sources[:3] if sources else []
        })
        
    except Exception as e:
        print(f"[ERROR] Question processing failed: {e}")
        return jsonify({
            'answer': 'Sorry, I encountered an error processing your question. Please try again.',
            'sources': []
        })

if __name__ == '__main__':
    print("Starting Enhanced Biosphere 2 RAG-Powered Web Interface...")
    print("Loading sensor data and initializing RAG database...")
    print("Web interface will be available at: http://localhost:5000")
    print("Advanced semantic search capabilities loading...")
    
    # Start background data loading
    threading.Thread(target=load_data_background, daemon=True).start()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
