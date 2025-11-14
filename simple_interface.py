import os
import pandas as pd
import json
from anthropic import Anthropic
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def load_all_sensor_data():
    """Load and analyze all CSV files in the data folder automatically"""
    import glob
    
    # Find all CSV files in data folder
    csv_files = glob.glob("data/*.csv")
    
    if not csv_files:
        print("[WARNING] No CSV files found in data folder!")
        return {}
    
    print(f"[INFO] Found {len(csv_files)} CSV files in data folder")
    
    all_data = {}
    
    for file_path in sorted(csv_files):
        try:
            # Extract sensor name from filename
            filename = os.path.basename(file_path)
            # Use filename without extension as sensor identifier
            sensor_id = filename.replace('.csv', '').lower()
            
            # Try to extract a more readable name from the file
            # Read first line to get sensor description
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    second_line = f.readline().strip()
            except:
                first_line = ""
                second_line = ""
            
            print(f"Loading {sensor_id}...")
            
            # Load CSV with proper encoding and error handling
            df = None
            try:
                # Try with UTF-8 encoding first
                try:
                    # Use on_bad_lines='skip' for pandas >= 1.3, or error_bad_lines=False for older versions
                    try:
                        df = pd.read_csv(file_path, encoding='utf-8', skiprows=2, on_bad_lines='skip', engine='python')
                    except TypeError:
                        # Fallback for older pandas versions
                        df = pd.read_csv(file_path, encoding='utf-8', skiprows=2, error_bad_lines=False, warn_bad_lines=False, engine='python')
                except UnicodeDecodeError:
                    # Try with latin-1 encoding
                    try:
                        df = pd.read_csv(file_path, encoding='latin-1', skiprows=2, on_bad_lines='skip', engine='python')
                    except TypeError:
                        df = pd.read_csv(file_path, encoding='latin-1', skiprows=2, error_bad_lines=False, warn_bad_lines=False, engine='python')
            except Exception as parse_error:
                # If all else fails, try with quotechar to handle commas in fields
                try:
                    df = pd.read_csv(file_path, encoding='utf-8', skiprows=2, quotechar='"', on_bad_lines='skip', engine='python')
                except:
                    try:
                        df = pd.read_csv(file_path, encoding='latin-1', skiprows=2, quotechar='"', on_bad_lines='skip', engine='python')
                    except:
                        raise parse_error
            
            if df is None or len(df) == 0:
                raise ValueError("Failed to load CSV or file is empty")
            
            # Get basic statistics
            stats = {
                "filename": filename,
                "sensor_description": second_line if second_line else first_line,
                "total_readings": len(df),
                "time_range": f"{df[' TIMESTAMP'].iloc[0]} to {df[' TIMESTAMP'].iloc[-1]}" if len(df) > 0 and ' TIMESTAMP' in df.columns else "No data",
                "sample_data": df.head(5).to_dict('records') if len(df) > 0 else [],
                "columns": list(df.columns)
            }
            
            # Add value statistics for numeric columns
            if ' VALUE' in df.columns:
                # Convert to numeric, coercing errors to NaN
                numeric_values = pd.to_numeric(df[' VALUE'], errors='coerce')
                numeric_values = numeric_values.dropna()  # Remove NaN values
                
                if len(numeric_values) > 0:
                    stats["value_stats"] = {
                        "min": float(numeric_values.min()),
                        "max": float(numeric_values.max()),
                        "mean": float(numeric_values.mean())
                    }
                else:
                    stats["value_stats"] = {
                        "min": None,
                        "max": None,
                        "mean": None
                    }
            
            all_data[sensor_id] = stats
            print(f"[OK] {sensor_id}: {len(df)} readings")
            
        except Exception as e:
            print(f"[ERROR] Loading {file_path}: {e}")
            import traceback
            traceback.print_exc()
            all_data[sensor_id] = {"error": str(e), "filename": filename}
    
    print(f"[SUCCESS] Loaded {len(all_data)} sensor files")
    return all_data

def create_comprehensive_context(all_data):
    """Create comprehensive context from all sensor data"""
    total_sensors = len(all_data)
    total_readings = sum(data.get('total_readings', 0) for data in all_data.values() if 'error' not in data)
    
    context_summary = f"""
    BIOSPHERE 2 ENVIRONMENTAL CONTROL SYSTEM ANALYSIS
    
    This analysis covers {total_sensors} different sensor systems across multiple areas:
    - Total sensors: {total_sensors}
    - Total readings: {total_readings:,}
    
    SENSOR SUMMARY:
    """
    
    # Group sensors by type/area for better organization
    sensor_list = []
    for sensor_id, data in sorted(all_data.items()):
        if 'error' in data:
            continue
        
        sensor_desc = data.get('sensor_description', sensor_id)
        readings = data.get('total_readings', 0)
        time_range = data.get('time_range', 'Unknown')
        
        sensor_info = f"  - {sensor_id}: {sensor_desc}\n"
        sensor_info += f"    Readings: {readings}, Time Range: {time_range}"
        
        if 'value_stats' in data:
            stats = data['value_stats']
            if stats.get('min') is not None:
                sensor_info += f"\n    Value Range: {stats['min']} to {stats['max']} (avg: {stats['mean']:.2f})"
        
        sensor_list.append(sensor_info)
    
    context_summary += "\n".join(sensor_list)
    context_summary += "\n\nSAMPLE DATA FROM KEY SENSORS:\n"
    
    # Add sample data from first 10 sensors (to avoid too much data)
    sample_count = 0
    for sensor_id, data in sorted(all_data.items()):
        if sample_count >= 10:
            break
        if 'error' not in data and 'sample_data' in data and data['sample_data']:
            context_summary += f"\n{sensor_id.upper()} SAMPLE:\n"
            for i, record in enumerate(data['sample_data'][:2]):  # First 2 records
                context_summary += f"  Record {i+1}: {record}\n"
            sample_count += 1
    
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
            model="claude-3-haiku-20240307",
            max_tokens=200,  # Much shorter responses
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("=== BIOSPHERE 2 SENSOR DATA ANALYSIS ===")
    print("Loading and analyzing all sensor files in data folder...")
    
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
