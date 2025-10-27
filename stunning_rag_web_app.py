# Stunning Biosphere 2 RAG Web App with Amazing UI
# Ultra-Modern Design with Spectacular Visual Effects

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

# Spectacular HTML Template with Amazing Colors
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biosphere 2 RAG-Powered Sensor Analysis</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            min-height: 100vh;
            color: #2d3748;
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
        }
        
        .floating-shapes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }
        
        .shape {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            animation: float 20s infinite linear;
        }
        
        .shape:nth-child(1) {
            width: 80px;
            height: 80px;
            top: 20%;
            left: 10%;
            animation-delay: 0s;
        }
        
        .shape:nth-child(2) {
            width: 120px;
            height: 120px;
            top: 60%;
            right: 10%;
            animation-delay: -5s;
        }
        
        .shape:nth-child(3) {
            width: 60px;
            height: 60px;
            top: 80%;
            left: 20%;
            animation-delay: -10s;
        }
        
        .shape:nth-child(4) {
            width: 100px;
            height: 100px;
            top: 30%;
            right: 30%;
            animation-delay: -15s;
        }
        
        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
            100% { transform: translateY(0px) rotate(360deg); }
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
            position: relative;
            z-index: 10;
        }
        
        .header h1 {
            font-size: 4rem;
            font-weight: 800;
            margin-bottom: 15px;
            text-shadow: 0 4px 20px rgba(0,0,0,0.3);
            background: linear-gradient(45deg, #fff, #f0f0f0, #fff);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: textShine 3s ease-in-out infinite;
        }
        
        @keyframes textShine {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .header p {
            font-size: 1.4rem;
            opacity: 0.95;
            font-weight: 300;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 420px;
            gap: 30px;
            margin-bottom: 30px;
            position: relative;
            z-index: 10;
        }
        
        .chat-section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            padding: 35px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
            border: 1px solid rgba(255,255,255,0.3);
            position: relative;
            overflow: hidden;
        }
        
        .chat-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe);
            background-size: 300% 300%;
            animation: gradientShift 8s ease infinite;
        }
        
        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 25px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 28px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.3);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
            background-size: 200% 200%;
            animation: gradientShift 6s ease infinite;
        }
        
        .card h3 {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 20px;
            color: #2d3748;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .chat-container {
            height: 550px;
            overflow-y: auto;
            border: 2px solid rgba(102, 126, 234, 0.2);
            border-radius: 18px;
            padding: 25px;
            margin-bottom: 25px;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            position: relative;
        }
        
        .chat-container::-webkit-scrollbar {
            width: 8px;
        }
        
        .chat-container::-webkit-scrollbar-track {
            background: rgba(102, 126, 234, 0.1);
            border-radius: 4px;
        }
        
        .chat-container::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 4px;
        }
        
        .message {
            margin-bottom: 25px;
            animation: messageSlideIn 0.5s ease-out;
        }
        
        @keyframes messageSlideIn {
            from {
                opacity: 0;
                transform: translateY(30px) scale(0.95);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        .message.user {
            text-align: right;
        }
        
        .message.assistant {
            text-align: left;
        }
        
        .message-content {
            display: inline-block;
            max-width: 85%;
            padding: 18px 24px;
            border-radius: 25px;
            font-size: 1rem;
            line-height: 1.6;
            position: relative;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-bottom-right-radius: 8px;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }
        
        .message.assistant .message-content {
            background: white;
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-bottom-left-radius: 8px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }
        
        .message-time {
            font-size: 0.8rem;
            color: #718096;
            margin-top: 8px;
            font-weight: 500;
        }
        
        .input-container {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        .message-input {
            flex: 1;
            padding: 20px 25px;
            border: 2px solid rgba(102, 126, 234, 0.3);
            border-radius: 30px;
            font-size: 1.1rem;
            outline: none;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            font-weight: 500;
        }
        
        .message-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
            background: white;
        }
        
        .send-button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .send-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s ease;
        }
        
        .send-button:hover::before {
            left: 100%;
        }
        
        .send-button:hover {
            transform: scale(1.1);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
        }
        
        .send-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .quick-questions {
            display: grid;
            gap: 12px;
        }
        
        .quick-question {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 12px;
            padding: 16px 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.95rem;
            color: #4a5568;
            font-weight: 500;
            position: relative;
            overflow: hidden;
        }
        
        .quick-question::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
            transition: left 0.5s ease;
        }
        
        .quick-question:hover::before {
            left: 100%;
        }
        
        .quick-question:hover {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .stat-item {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border-radius: 12px;
            border: 1px solid rgba(102, 126, 234, 0.2);
            transition: all 0.3s ease;
        }
        
        .stat-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }
        
        .stat-label {
            font-size: 0.85rem;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 18px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .status-ready {
            background: linear-gradient(135deg, rgba(72, 187, 120, 0.2), rgba(56, 178, 172, 0.2));
            color: #22543d;
            border: 1px solid rgba(72, 187, 120, 0.3);
        }
        
        .status-loading {
            background: linear-gradient(135deg, rgba(245, 101, 101, 0.2), rgba(251, 146, 60, 0.2));
            color: #742a2a;
            border: 1px solid rgba(245, 101, 101, 0.3);
        }
        
        .status-error {
            background: linear-gradient(135deg, rgba(245, 101, 101, 0.3), rgba(220, 38, 38, 0.3));
            color: #742a2a;
            border: 1px solid rgba(245, 101, 101, 0.4);
        }
        
        .loading-spinner {
            width: 20px;
            height: 20px;
            border: 3px solid rgba(102, 126, 234, 0.2);
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        .sources-section {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid rgba(102, 126, 234, 0.1);
        }
        
        .sources-title {
            font-size: 0.9rem;
            font-weight: 700;
            color: #4a5568;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .source-item {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
            border: 1px solid rgba(102, 126, 234, 0.1);
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 8px;
            font-size: 0.85rem;
            color: #4a5568;
            transition: all 0.3s ease;
        }
        
        .source-item:hover {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            transform: translateX(5px);
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .typing-indicator {
            display: none;
            padding: 16px 20px;
            background: white;
            border: 2px solid rgba(102, 126, 234, 0.2);
            border-radius: 25px;
            border-bottom-left-radius: 8px;
            margin-bottom: 25px;
            max-width: 100px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }
        
        .typing-dots {
            display: flex;
            gap: 6px;
        }
        
        .typing-dot {
            width: 10px;
            height: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
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
                transform: scale(1.2);
                opacity: 1;
            }
        }
        
        .pulse-effect {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
            100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
                gap: 25px;
            }
            
            .header h1 {
                font-size: 2.5rem;
            }
            
            .chat-container {
                height: 450px;
            }
            
            .message-content {
                max-width: 90%;
            }
            
            .container {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="floating-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    
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
                            <ul style="margin: 12px 0; padding-left: 25px;">
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
                    <button class="send-button pulse-effect" id="sendButton" onclick="sendMessage()">
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
            
            // Add some visual flair
            addSparkleEffect();
        });
        
        function addSparkleEffect() {
            const sparkle = document.createElement('div');
            sparkle.style.cssText = `
                position: fixed;
                width: 4px;
                height: 4px;
                background: white;
                border-radius: 50%;
                pointer-events: none;
                z-index: 1000;
                animation: sparkle 2s linear infinite;
            `;
            document.body.appendChild(sparkle);
            
            setInterval(() => {
                sparkle.style.left = Math.random() * window.innerWidth + 'px';
                sparkle.style.top = Math.random() * window.innerHeight + 'px';
            }, 2000);
        }
        
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
    
    <style>
        @keyframes sparkle {
            0% { opacity: 0; transform: scale(0); }
            50% { opacity: 1; transform: scale(1); }
            100% { opacity: 0; transform: scale(0); }
        }
    </style>
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
    print("Starting Stunning Biosphere 2 RAG-Powered Web Interface...")
    print("Loading sensor data and initializing RAG database...")
    print("Web interface will be available at: http://localhost:5000")
    print("Spectacular visual effects and animations loading...")
    
    # Start background data loading
    threading.Thread(target=load_data_background, daemon=True).start()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

