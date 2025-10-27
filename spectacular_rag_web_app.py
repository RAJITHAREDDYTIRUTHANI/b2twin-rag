# Spectacular Biosphere 2 RAG Web App with Amazing Colors
# Ultra-Vibrant Neon Cyberpunk Design

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
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Exo 2', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
            background-size: 400% 400%;
            animation: gradientShift 20s ease infinite;
            min-height: 100vh;
            color: #e0e6ed;
            line-height: 1.6;
            overflow-x: hidden;
            position: relative;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
            pointer-events: none;
            z-index: 1;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 10;
        }
        
        .floating-particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 2;
        }
        
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: linear-gradient(45deg, #00ffff, #ff00ff);
            border-radius: 50%;
            animation: floatParticle 15s infinite linear;
            box-shadow: 0 0 10px currentColor;
        }
        
        .particle:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
        .particle:nth-child(2) { top: 20%; left: 80%; animation-delay: -2s; }
        .particle:nth-child(3) { top: 60%; left: 20%; animation-delay: -4s; }
        .particle:nth-child(4) { top: 80%; left: 70%; animation-delay: -6s; }
        .particle:nth-child(5) { top: 30%; left: 50%; animation-delay: -8s; }
        .particle:nth-child(6) { top: 70%; left: 90%; animation-delay: -10s; }
        
        @keyframes floatParticle {
            0% { transform: translateY(0px) translateX(0px) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-100px) translateX(50px) rotate(360deg); opacity: 0; }
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
            color: white;
            position: relative;
            z-index: 10;
        }
        
        .header h1 {
            font-family: 'Orbitron', monospace;
            font-size: 4.5rem;
            font-weight: 900;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00, #00ff00);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: neonGlow 3s ease-in-out infinite, textShine 4s ease-in-out infinite;
            text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
            letter-spacing: 2px;
        }
        
        @keyframes neonGlow {
            0%, 100% { 
                text-shadow: 0 0 30px rgba(0, 255, 255, 0.5),
                            0 0 60px rgba(255, 0, 255, 0.3),
                            0 0 90px rgba(255, 255, 0, 0.2);
            }
            50% { 
                text-shadow: 0 0 40px rgba(255, 0, 255, 0.6),
                            0 0 80px rgba(0, 255, 255, 0.4),
                            0 0 120px rgba(255, 255, 0, 0.3);
            }
        }
        
        @keyframes textShine {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .header p {
            font-size: 1.5rem;
            opacity: 0.9;
            font-weight: 300;
            color: #a0a8b0;
            text-shadow: 0 0 20px rgba(160, 168, 176, 0.3);
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 450px;
            gap: 35px;
            margin-bottom: 35px;
            position: relative;
            z-index: 10;
        }
        
        .chat-section {
            background: rgba(15, 15, 35, 0.8);
            backdrop-filter: blur(25px);
            border-radius: 30px;
            padding: 40px;
            box-shadow: 
                0 30px 60px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(0, 255, 255, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .chat-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #00ffff, #ff00ff, #ffff00, #00ff00, #00ffff);
            background-size: 400% 400%;
            animation: gradientShift 6s ease infinite;
        }
        
        .chat-section::after {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00, #00ff00);
            background-size: 400% 400%;
            border-radius: 30px;
            z-index: -1;
            animation: gradientShift 8s ease infinite;
            opacity: 0.3;
        }
        
        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 30px;
        }
        
        .card {
            background: rgba(15, 15, 35, 0.7);
            backdrop-filter: blur(25px);
            border-radius: 25px;
            padding: 32px;
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 0, 255, 0.2);
            position: relative;
            overflow: hidden;
            transition: all 0.4s ease;
        }
        
        .card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 
                0 30px 60px rgba(0, 0, 0, 0.3),
                0 0 30px rgba(255, 0, 255, 0.2);
            border-color: rgba(255, 0, 255, 0.4);
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #ff00ff, #00ffff, #ffff00);
            background-size: 300% 300%;
            animation: gradientShift 5s ease infinite;
        }
        
        .card h3 {
            font-family: 'Orbitron', monospace;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 25px;
            color: #00ffff;
            display: flex;
            align-items: center;
            gap: 12px;
            text-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        }
        
        .chat-container {
            height: 600px;
            overflow-y: auto;
            border: 2px solid rgba(0, 255, 255, 0.3);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            background: rgba(0, 0, 0, 0.3);
            position: relative;
        }
        
        .chat-container::-webkit-scrollbar {
            width: 10px;
        }
        
        .chat-container::-webkit-scrollbar-track {
            background: rgba(0, 255, 255, 0.1);
            border-radius: 5px;
        }
        
        .chat-container::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #00ffff, #ff00ff);
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
        }
        
        .message {
            margin-bottom: 30px;
            animation: messageSlideIn 0.6s ease-out;
        }
        
        @keyframes messageSlideIn {
            from {
                opacity: 0;
                transform: translateY(40px) scale(0.9);
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
            padding: 20px 28px;
            border-radius: 30px;
            font-size: 1.05rem;
            line-height: 1.7;
            position: relative;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #00ffff, #0080ff);
            color: #000;
            border-bottom-right-radius: 10px;
            box-shadow: 
                0 10px 30px rgba(0, 255, 255, 0.3),
                0 0 20px rgba(0, 255, 255, 0.5);
            font-weight: 600;
        }
        
        .message.assistant .message-content {
            background: rgba(255, 255, 255, 0.95);
            color: #1a1a2e;
            border-bottom-left-radius: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 0, 255, 0.2);
        }
        
        .message-time {
            font-size: 0.85rem;
            color: #a0a8b0;
            margin-top: 10px;
            font-weight: 500;
            text-shadow: 0 0 10px rgba(160, 168, 176, 0.3);
        }
        
        .input-container {
            display: flex;
            gap: 18px;
            align-items: center;
        }
        
        .message-input {
            flex: 1;
            padding: 22px 30px;
            border: 2px solid rgba(0, 255, 255, 0.4);
            border-radius: 35px;
            font-size: 1.1rem;
            outline: none;
            transition: all 0.4s ease;
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(15px);
            font-weight: 500;
            color: #e0e6ed;
        }
        
        .message-input::placeholder {
            color: #a0a8b0;
        }
        
        .message-input:focus {
            border-color: #00ffff;
            box-shadow: 
                0 0 0 5px rgba(0, 255, 255, 0.2),
                0 0 30px rgba(0, 255, 255, 0.3);
            background: rgba(0, 0, 0, 0.6);
        }
        
        .send-button {
            background: linear-gradient(135deg, #ff00ff, #00ffff);
            color: #000;
            border: none;
            border-radius: 50%;
            width: 70px;
            height: 70px;
            cursor: pointer;
            transition: all 0.4s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: 
                0 10px 30px rgba(255, 0, 255, 0.4),
                0 0 20px rgba(0, 255, 255, 0.3);
            position: relative;
            overflow: hidden;
            font-weight: 900;
        }
        
        .send-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transition: left 0.6s ease;
        }
        
        .send-button:hover::before {
            left: 100%;
        }
        
        .send-button:hover {
            transform: scale(1.15) rotate(5deg);
            box-shadow: 
                0 15px 40px rgba(255, 0, 255, 0.5),
                0 0 30px rgba(0, 255, 255, 0.4);
        }
        
        .send-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .quick-questions {
            display: grid;
            gap: 15px;
        }
        
        .quick-question {
            background: rgba(255, 0, 255, 0.1);
            border: 1px solid rgba(255, 0, 255, 0.3);
            border-radius: 15px;
            padding: 18px 24px;
            cursor: pointer;
            transition: all 0.4s ease;
            font-size: 1rem;
            color: #e0e6ed;
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
            background: linear-gradient(90deg, transparent, rgba(255, 0, 255, 0.2), transparent);
            transition: left 0.6s ease;
        }
        
        .quick-question:hover::before {
            left: 100%;
        }
        
        .quick-question:hover {
            background: rgba(255, 0, 255, 0.2);
            border-color: #ff00ff;
            transform: translateY(-3px);
            box-shadow: 
                0 10px 30px rgba(255, 0, 255, 0.3),
                0 0 20px rgba(255, 0, 255, 0.2);
            color: #fff;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
        }
        
        .stat-item {
            text-align: center;
            padding: 25px;
            background: rgba(0, 255, 255, 0.1);
            border-radius: 15px;
            border: 1px solid rgba(0, 255, 255, 0.3);
            transition: all 0.4s ease;
        }
        
        .stat-item:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 
                0 15px 35px rgba(0, 255, 255, 0.3),
                0 0 25px rgba(0, 255, 255, 0.2);
        }
        
        .stat-value {
            font-family: 'Orbitron', monospace;
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #00ffff, #ff00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #a0a8b0;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 700;
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 15px 22px;
            border-radius: 30px;
            font-size: 1rem;
            font-weight: 700;
            transition: all 0.4s ease;
        }
        
        .status-ready {
            background: rgba(0, 255, 0, 0.2);
            color: #00ff00;
            border: 1px solid rgba(0, 255, 0, 0.4);
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
        }
        
        .status-loading {
            background: rgba(255, 255, 0, 0.2);
            color: #ffff00;
            border: 1px solid rgba(255, 255, 0, 0.4);
            box-shadow: 0 0 20px rgba(255, 255, 0, 0.3);
        }
        
        .status-error {
            background: rgba(255, 0, 0, 0.2);
            color: #ff0000;
            border: 1px solid rgba(255, 0, 0, 0.4);
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
        }
        
        .loading-spinner {
            width: 25px;
            height: 25px;
            border: 4px solid rgba(0, 255, 255, 0.2);
            border-top: 4px solid #00ffff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        }
        
        .sources-section {
            margin-top: 25px;
            padding-top: 25px;
            border-top: 2px solid rgba(0, 255, 255, 0.2);
        }
        
        .sources-title {
            font-size: 1rem;
            font-weight: 800;
            color: #00ffff;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        }
        
        .source-item {
            background: rgba(0, 255, 255, 0.05);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 10px;
            padding: 15px 20px;
            margin-bottom: 10px;
            font-size: 0.9rem;
            color: #a0a8b0;
            transition: all 0.4s ease;
        }
        
        .source-item:hover {
            background: rgba(0, 255, 255, 0.1);
            transform: translateX(8px);
            border-color: rgba(0, 255, 255, 0.4);
            color: #e0e6ed;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .typing-indicator {
            display: none;
            padding: 20px 25px;
            background: rgba(255, 255, 255, 0.95);
            border: 2px solid rgba(0, 255, 255, 0.3);
            border-radius: 30px;
            border-bottom-left-radius: 10px;
            margin-bottom: 30px;
            max-width: 120px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        .typing-dots {
            display: flex;
            gap: 8px;
        }
        
        .typing-dot {
            width: 12px;
            height: 12px;
            background: linear-gradient(135deg, #00ffff, #ff00ff);
            border-radius: 50%;
            animation: typing 1.4s infinite ease-in-out;
            box-shadow: 0 0 10px currentColor;
        }
        
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes typing {
            0%, 80%, 100% {
                transform: scale(0.8);
                opacity: 0.5;
            }
            40% {
                transform: scale(1.3);
                opacity: 1;
            }
        }
        
        .pulse-effect {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(255, 0, 255, 0.4); }
            70% { box-shadow: 0 0 0 15px rgba(255, 0, 255, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 0, 255, 0); }
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
                gap: 30px;
            }
            
            .header h1 {
                font-size: 3rem;
            }
            
            .chat-container {
                height: 500px;
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
    <div class="floating-particles">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
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
                            <ul style="margin: 15px 0; padding-left: 30px;">
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
            for (let i = 0; i < 20; i++) {
                setTimeout(() => {
                    const sparkle = document.createElement('div');
                    sparkle.style.cssText = `
                        position: fixed;
                        width: 6px;
                        height: 6px;
                        background: linear-gradient(45deg, #00ffff, #ff00ff);
                        border-radius: 50%;
                        pointer-events: none;
                        z-index: 1000;
                        animation: sparkle 3s linear infinite;
                        box-shadow: 0 0 15px currentColor;
                    `;
                    sparkle.style.left = Math.random() * window.innerWidth + 'px';
                    sparkle.style.top = Math.random() * window.innerHeight + 'px';
                    document.body.appendChild(sparkle);
                    
                    setTimeout(() => sparkle.remove(), 3000);
                }, i * 150);
            }
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
            0% { opacity: 0; transform: scale(0) rotate(0deg); }
            50% { opacity: 1; transform: scale(1) rotate(180deg); }
            100% { opacity: 0; transform: scale(0) rotate(360deg); }
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
    print("Starting Spectacular Biosphere 2 RAG-Powered Web Interface...")
    print("Loading sensor data and initializing RAG database...")
    print("Web interface will be available at: http://localhost:5000")
    print("Amazing neon cyberpunk visual effects loading...")
    
    # Start background data loading
    threading.Thread(target=load_data_background, daemon=True).start()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

