from flask import Flask, render_template_string, request, jsonify
import json
import os
from main import ask_question, load_all_sensor_data, create_comprehensive_analysis

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biosphere 2 Sensor Data Analysis</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #2c5530, #4a7c59);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .card h2 {
            color: #2c5530;
            margin-top: 0;
            border-bottom: 2px solid #4a7c59;
            padding-bottom: 10px;
        }
        .question-form {
            margin-bottom: 20px;
        }
        .question-input {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 15px;
            box-sizing: border-box;
        }
        .question-input:focus {
            outline: none;
            border-color: #4a7c59;
        }
        .submit-btn {
            background: linear-gradient(135deg, #4a7c59, #2c5530);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .submit-btn:hover {
            transform: translateY(-2px);
        }
        .answer {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #4a7c59;
            margin-top: 20px;
            white-space: pre-wrap;
        }
        .sensor-info {
            background: #e8f5e8;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .sensor-info h3 {
            margin: 0 0 10px 0;
            color: #2c5530;
        }
        .sensor-info p {
            margin: 5px 0;
            font-size: 14px;
        }
        .loading {
            text-align: center;
            color: #666;
            font-style: italic;
        }
        .error {
            background: #ffe6e6;
            color: #d63031;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #d63031;
        }
        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌿 Biosphere 2 Sensor Data Analysis</h1>
        <p>Interactive Environmental Monitoring System</p>
    </div>

    <div class="container">
        <div class="card">
            <h2>Ask Questions About Sensor Data</h2>
            <form method="post" class="question-form">
                <input type="text" name="question" class="question-input" 
                       placeholder="Ask a question about the Biosphere 2 sensor data..." required>
                <button type="submit" class="submit-btn">Ask Question</button>
            </form>
            
            {% if answer %}
            <div class="answer">
                <strong>Answer:</strong><br>
                {{ answer }}
            </div>
            {% endif %}
            
            {% if error %}
            <div class="error">
                {{ error }}
            </div>
            {% endif %}
        </div>

        <div class="card">
            <h2>Sensor Systems Overview</h2>
            {% for sensor_type, data in sensor_data.items() %}
            <div class="sensor-info">
                <h3>{{ sensor_type.replace('_', ' ').title() }}</h3>
                <p><strong>Readings:</strong> {{ data.total_readings }}</p>
                <p><strong>Time Range:</strong> {{ data.time_range }}</p>
                {% if data.value_stats %}
                <p><strong>Value Range:</strong> {{ "%.2f"|format(data.value_stats.min) }} to {{ "%.2f"|format(data.value_stats.max) }}</p>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </div>

    <script>
        // Auto-focus on question input
        document.querySelector('.question-input').focus();
        
        // Handle form submission with loading state
        document.querySelector('form').addEventListener('submit', function() {
            const submitBtn = document.querySelector('.submit-btn');
            submitBtn.textContent = 'Analyzing...';
            submitBtn.disabled = true;
        });
    </script>
</body>
</html>
"""

# Global variables to store data
sensor_data = {}
context_summary = ""

@app.route('/', methods=['GET', 'POST'])
def home():
    global sensor_data, context_summary
    
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        
        if not question:
            return render_template_string(HTML_TEMPLATE, 
                                        sensor_data=sensor_data, 
                                        answer=None, 
                                        error="Please enter a question.")
        
        try:
            # Get answer from Claude
            answer = ask_question(question, context_summary)
            return render_template_string(HTML_TEMPLATE, 
                                        sensor_data=sensor_data, 
                                        answer=answer, 
                                        error=None)
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, 
                                        sensor_data=sensor_data, 
                                        answer=None, 
                                        error=f"Error processing question: {str(e)}")
    
    # GET request - show the form
    return render_template_string(HTML_TEMPLATE, 
                                sensor_data=sensor_data, 
                                answer=None, 
                                error=None)

@app.route('/api/data')
def get_sensor_data():
    """API endpoint to get sensor data as JSON"""
    return jsonify(sensor_data)

if __name__ == "__main__":
    print("Loading Biosphere 2 sensor data...")
    sensor_data, context_summary = create_comprehensive_analysis()
    print("Web interface ready!")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
