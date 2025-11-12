import os
import pandas as pd
import json
from anthropic import Anthropic
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def load_all_sensor_data():
    """Load and analyze all 6 CSV files to create comprehensive context"""
    data_files = {
        "temperature": "data/UAB2_BIO1_B4000_MISCSAV1_RFTESCOSUPTMP_327662.csv",
        "fan_direction": "data/UAB2_BIO1_B4000_MISCSAV1_RFTESCOVFDDIRCMD_322444.csv", 
        "fan_output": "data/UAB2_BIO1_B4000_MISCSAV1_RFTESCOVFDOUT_317704.csv",
        "fan_status": "data/UAB2_BIO1_B4000_MISCSAV1_RFTESCOVFDSTS_310102.csv",
        "valve_command": "data/UAB2_BIO1_B4000_MISCSAV1_RFTESCOVLVCMD_314109.csv",
        "valve_limit": "data/UAB2_BIO1_B4000_MISCSAV1_RFTESCOVLVLMTSW_305745.csv"
    }
    
    all_data = {}
    
    for sensor_type, file_path in data_files.items():
        try:
            print(f"Loading {sensor_type}...")
            # Load CSV with proper encoding
            try:
                df = pd.read_csv(file_path, encoding='utf-8', skiprows=2)
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='latin-1', skiprows=2)
            
            # Get basic statistics
            stats = {
                "total_readings": len(df),
                "time_range": f"{df[' TIMESTAMP'].iloc[0]} to {df[' TIMESTAMP'].iloc[-1]}" if len(df) > 0 else "No data",
                "sample_data": df.head(5).to_dict('records') if len(df) > 0 else [],
                "columns": list(df.columns)
            }
            
            # Add value statistics for numeric columns
            if ' VALUE' in df.columns:
                stats["value_stats"] = {
                    "min": float(df[' VALUE'].min()) if len(df) > 0 else None,
                    "max": float(df[' VALUE'].max()) if len(df) > 0 else None,
                    "mean": float(df[' VALUE'].mean()) if len(df) > 0 else None
                }
            
            all_data[sensor_type] = stats
            print(f"[OK] {sensor_type}: {len(df)} readings")
            
        except Exception as e:
            print(f"[ERROR] Loading {file_path}: {e}")
            all_data[sensor_type] = {"error": str(e)}
    
    return all_data

def create_comprehensive_context(all_data):
    """Create comprehensive context from all sensor data"""
    context_summary = f"""
    BIOSPHERE 2 ENVIRONMENTAL CONTROL SYSTEM ANALYSIS
    
    This analysis covers 6 different sensor systems monitoring the Rainforest MiscSAV1 area:
    
    1. TEMPERATURE SENSOR (RFTESCOSUPTMP):
       - Units: Fahrenheit
       - Readings: {all_data.get('temperature', {}).get('total_readings', 'N/A')}
       - Time Range: {all_data.get('temperature', {}).get('time_range', 'N/A')}
       - Value Range: {all_data.get('temperature', {}).get('value_stats', {}).get('min', 'N/A')}°F to {all_data.get('temperature', {}).get('value_stats', {}).get('max', 'N/A')}°F
    
    2. FAN DIRECTION COMMAND (RFTESCOVFDDIRCMD):
       - Control: Exhaust/Injection modes
       - Readings: {all_data.get('fan_direction', {}).get('total_readings', 'N/A')}
       - Time Range: {all_data.get('fan_direction', {}).get('time_range', 'N/A')}
    
    3. FAN OUTPUT CONTROL (RFTESCOVFDOUT):
       - Control: ON/OFF states
       - Readings: {all_data.get('fan_output', {}).get('total_readings', 'N/A')}
       - Time Range: {all_data.get('fan_output', {}).get('time_range', 'N/A')}
    
    4. FAN STATUS MONITORING (RFTESCOVFDSTS):
       - Status: ON/OFF states
       - Readings: {all_data.get('fan_status', {}).get('total_readings', 'N/A')}
       - Time Range: {all_data.get('fan_status', {}).get('time_range', 'N/A')}
    
    5. VALVE COMMAND CONTROL (RFTESCOVLVCMD):
       - Control: ON/OFF commands
       - Readings: {all_data.get('valve_command', {}).get('total_readings', 'N/A')}
       - Time Range: {all_data.get('valve_command', {}).get('time_range', 'N/A')}
    
    6. VALVE LIMIT SWITCH (RFTESCOVLVLMTSW):
       - Status: CLOSED/OPEN positions
       - Readings: {all_data.get('valve_limit', {}).get('total_readings', 'N/A')}
       - Time Range: {all_data.get('valve_limit', {}).get('time_range', 'N/A')}
    
    SAMPLE DATA FROM EACH SYSTEM:
    """
    
    # Add sample data from each system
    for sensor_type, data in all_data.items():
        if 'sample_data' in data and data['sample_data']:
            context_summary += f"\n{sensor_type.upper()} SAMPLE:\n"
            for i, record in enumerate(data['sample_data'][:3]):  # First 3 records
                context_summary += f"  Record {i+1}: {record}\n"
    
    return context_summary

def ask_question(question, context_data):
    """Ask a question about the sensor data using Claude"""
    prompt = f"""
    You are a Biosphere 2 environmental analyst. Give short, crisp answers based on the sensor data.

    DATA: {context_data}

    QUESTION: {question}

    RULES:
    - Answer in 1-2 sentences maximum
    - Use specific numbers from the data
    - Be direct and actionable
    - If data is missing, say "No [specific data] available"
    - Focus on what the data shows, not what it doesn't
    """
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,  # Much shorter responses
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("=== BIOSPHERE 2 SENSOR DATA ANALYSIS ===")
    print("Loading and analyzing all 6 sensor systems...")
    
    # Load all sensor data
    all_data = load_all_sensor_data()
    
    # Create comprehensive context
    context_summary = create_comprehensive_context(all_data)
    
    # Save context to file
    os.makedirs("results", exist_ok=True)
    with open("results/comprehensive_context.txt", "w", encoding="utf-8") as f:
        f.write(context_summary)
    
    # Save structured data as JSON
    with open("results/sensor_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, default=str)
    
    print("\n[SUCCESS] All sensor data analyzed and context created!")
    print("Files generated:")
    print("- results/comprehensive_context.txt (human-readable summary)")
    print("- results/sensor_data.json (structured data)")
    
    print("\n=== INTERACTIVE QUESTION MODE ===")
    print("You can now ask questions about the Biosphere 2 sensor data.")
    print("Type 'quit' to exit.\n")
    
    while True:
        question = input("Ask a question about the sensor data: ").strip()
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        if question:
            print("\nAnalyzing your question...")
            answer = ask_question(question, context_summary)
            print(f"\nAnswer: {answer}\n")
        else:
            print("Please enter a question.\n")
