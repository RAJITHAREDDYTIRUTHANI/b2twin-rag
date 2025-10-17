from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import json
import os
from simple_interface import ask_question, load_all_sensor_data, create_comprehensive_context
import threading
import time

app = Flask(__name__)

# Global variables to store data
sensor_data = {}
context_summary = ""
data_loaded = False

# HTML template with modern design
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biosphere 2 Sensor Analysis</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
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
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
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
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .chat-header i {
            font-size: 1.5rem;
            color: #667eea;
            margin-right: 10px;
        }
        
        .chat-header h2 {
            color: #333;
            font-size: 1.5rem;
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
        
        .info-card h3 i {
            color: #667eea;
        }
        
        .sensor-item {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }
        
        .sensor-item h4 {
            color: #333;
            margin-bottom: 5px;
        }
        
        .sensor-item p {
            color: #666;
            font-size: 0.9rem;
        }
        
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-ok { background: #4caf50; }
        .status-warning { background: #ff9800; }
        .status-error { background: #f44336; }
        
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
            
            .container {
                padding: 10px;
            }
        }
        
        .footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-leaf"></i> Biosphere 2 Sensor Analysis</h1>
            <p>Interactive Environmental Monitoring System</p>
        </div>
        
        <div class="main-content">
            <div class="chat-container">
                <div class="chat-header">
                    <i class="fas fa-comments"></i>
                    <h2>Ask Questions About Your Sensor Data</h2>
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <div class="message system">
                        <i class="fas fa-robot"></i> System loaded successfully! Ask me anything about your Biosphere 2 sensor data.
                    </div>
                </div>
                
                <div class="loading" id="loading">
                    <i class="fas fa-spinner fa-spin"></i> Analyzing your question...
                </div>
                
                <div class="input-container">
                    <input type="text" id="questionInput" class="question-input" 
                           placeholder="Ask a question about your sensor data..." 
                           onkeypress="handleKeyPress(event)">
                    <button id="askBtn" class="ask-btn" onclick="askQuestion()">
                        <i class="fas fa-paper-plane"></i> Ask
                    </button>
                </div>
            </div>
            
            <div class="sidebar">
                <div class="info-card">
                    <h3><i class="fas fa-chart-line"></i> Sensor Overview</h3>
                    {% for sensor_type, data in sensor_data.items() %}
                    <div class="sensor-item">
                        <h4>
                            <span class="status-indicator status-ok"></span>
                            {{ sensor_type.replace('_', ' ').title() }}
                        </h4>
                        <p><strong>Readings:</strong> {{ data.total_readings }}</p>
                        <p><strong>Period:</strong> {{ data.time_range }}</p>
                        {% if data.value_stats %}
                        <p><strong>Range:</strong> {{ "%.1f"|format(data.value_stats.min) }}°F - {{ "%.1f"|format(data.value_stats.max) }}°F</p>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
                
                <div class="quick-questions">
                    <h3><i class="fas fa-lightning-bolt"></i> Quick Questions</h3>
                    <div class="quick-question" onclick="askQuickQuestion('What is the temperature range?')">
                        What is the temperature range?
                    </div>
                    <div class="quick-question" onclick="askQuickQuestion('How many readings were recorded?')">
                        How many readings were recorded?
                    </div>
                    <div class="quick-question" onclick="askQuickQuestion('What is the fan status?')">
                        What is the fan status?
                    </div>
                    <div class="quick-question" onclick="askQuickQuestion('Are there any errors?')">
                        Are there any errors?
                    </div>
                    <div class="quick-question" onclick="askQuickQuestion('What is the highest temperature?')">
                        What is the highest temperature?
                    </div>
                    <div class="quick-question" onclick="askQuickQuestion('What is the monitoring period?')">
                        What is the monitoring period?
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p><i class="fas fa-server"></i> Biosphere 2 Environmental Monitoring System | Ready for Jetstream2 Deployment</p>
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
            
            // Add user message
            addMessage(question, 'user');
            
            // Clear input and show loading
            input.value = '';
            showLoading(true);
            
            // Send question to server
            fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({question: question})
            })
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                addMessage(data.answer, 'assistant');
            })
            .catch(error => {
                showLoading(false);
                addMessage('Sorry, there was an error processing your question.', 'assistant');
                console.error('Error:', error);
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
        
        // Auto-focus on input
        document.getElementById('questionInput').focus();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Display the main interface"""
    return render_template_string(HTML_TEMPLATE, sensor_data=sensor_data)

@app.route('/ask', methods=['POST'])
def ask_question_endpoint():
    """Handle question submissions via AJAX"""
    global context_summary
    
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'answer': 'Please enter a question.'})
        
        # Get answer from Claude
        answer = ask_question(question, context_summary)
        
        return jsonify({'answer': answer})
        
    except Exception as e:
        return jsonify({'answer': f'Error processing question: {str(e)}'})

@app.route('/api/data')
def get_sensor_data():
    """API endpoint to get sensor data as JSON"""
    return jsonify(sensor_data)

@app.route('/api/status')
def get_status():
    """API endpoint to check system status"""
    return jsonify({
        'status': 'ready' if data_loaded else 'loading',
        'sensors': len(sensor_data),
        'data_points': sum(data.get('total_readings', 0) for data in sensor_data.values())
    })

def load_data_background():
    """Load sensor data in background"""
    global sensor_data, context_summary, data_loaded
    
    print("Loading Biosphere 2 sensor data...")
    all_data = load_all_sensor_data()
    sensor_data = all_data
    context_summary = create_comprehensive_context(all_data)
    data_loaded = True
    print("[SUCCESS] Data loaded successfully!")

if __name__ == "__main__":
    # Load data in background thread
    data_thread = threading.Thread(target=load_data_background)
    data_thread.daemon = True
    data_thread.start()
    
    print("Starting Biosphere 2 Sensor Analysis Web Interface...")
    print("Loading sensor data in background...")
    print("Web interface will be available at: http://localhost:5000")
    print("Ready for Jetstream2 deployment!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
