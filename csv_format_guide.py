# Rainforest Table Analysis - CSV Format Guide
# Understanding the expected format for your 26 tables

import pandas as pd
import os

def create_sample_csv():
    """Create sample CSV files to show expected format"""
    
    print("📋 Creating sample CSV format examples...")
    
    # Sample 1: Sensor data table
    sensor_data = {
        'ID': [1, 2, 3, 4, 5],
        'TIMESTAMP': ['2025/09/21 00:00:01', '2025/09/21 00:15:01', '2025/09/21 00:30:01', '2025/09/21 00:45:01', '2025/09/21 01:00:01'],
        'VALUE': [77.21, 77.16, 77.18, 77.07, 77.06],
        'STATUS': [0, 0, 0, 0, 0],
        'STATUS_TAG': ['{ok}', '{ok}', '{ok}', '{ok}', '{ok}'],
        'TRENDFLAGS': [0, 0, 0, 0, 0],
        'TRENDFLAGS_TAG': ['{ }', '{ }', '{ }', '{ }', '{ }']
    }
    
    df_sensor = pd.DataFrame(sensor_data)
    df_sensor.to_csv('rainforest_tables/sample_sensor_table.csv', index=False)
    
    # Sample 2: Control system table
    control_data = {
        'DEVICE_ID': ['FAN_001', 'FAN_002', 'VALVE_001', 'VALVE_002'],
        'COMMAND': ['ON', 'OFF', 'OPEN', 'CLOSED'],
        'STATUS': ['ACTIVE', 'INACTIVE', 'OPEN', 'CLOSED'],
        'TIMESTAMP': ['2025/09/21 10:00:00', '2025/09/21 10:15:00', '2025/09/21 10:30:00', '2025/09/21 10:45:00'],
        'VALUE': [1, 0, 1, 0],
        'UNITS': ['ON/OFF', 'ON/OFF', 'OPEN/CLOSED', 'OPEN/CLOSED']
    }
    
    df_control = pd.DataFrame(control_data)
    df_control.to_csv('rainforest_tables/sample_control_table.csv', index=False)
    
    # Sample 3: Environmental monitoring table
    env_data = {
        'SENSOR_ID': ['TEMP_001', 'HUMID_001', 'PRESS_001', 'CO2_001'],
        'MEASUREMENT_TYPE': ['Temperature', 'Humidity', 'Pressure', 'CO2'],
        'VALUE': [75.5, 65.2, 1013.25, 400],
        'UNITS': ['Fahrenheit', 'Percent', 'mbar', 'ppm'],
        'LOCATION': ['Zone_A', 'Zone_A', 'Zone_A', 'Zone_A'],
        'TIMESTAMP': ['2025/09/21 12:00:00', '2025/09/21 12:00:00', '2025/09/21 12:00:00', '2025/09/21 12:00:00'],
        'QUALITY': ['GOOD', 'GOOD', 'GOOD', 'GOOD']
    }
    
    df_env = pd.DataFrame(env_data)
    df_env.to_csv('rainforest_tables/sample_environmental_table.csv', index=False)
    
    print("✅ Sample CSV files created:")
    print("  - rainforest_tables/sample_sensor_table.csv")
    print("  - rainforest_tables/sample_control_table.csv")
    print("  - rainforest_tables/sample_environmental_table.csv")

def analyze_sample_files():
    """Analyze the sample files to show what the analyzer does"""
    
    print("\n🔍 Analyzing sample files...")
    
    from rainforest_analyzer import RainforestTableAnalyzer
    analyzer = RainforestTableAnalyzer()
    
    sample_tables = [
        "sample_sensor_table",
        "sample_control_table", 
        "sample_environmental_table"
    ]
    
    results = analyzer.analyze_multiple_tables(sample_tables)
    
    print("\n📊 Sample Analysis Results:")
    for table_name, analysis in results.items():
        if "error" not in analysis:
            print(f"\n📋 {table_name}:")
            print(f"  Rows: {analysis['total_rows']}")
            print(f"  Columns: {analysis['total_columns']}")
            
            print("  Column Analysis:")
            for col_name, col_analysis in analysis["column_analysis"].items():
                print(f"    {col_name}: {col_analysis['purpose_hint']} ({col_analysis['data_type']})")

def show_csv_format_guide():
    """Show guide for CSV format expectations"""
    
    print("\n📋 CSV Format Guide for Your 26 Tables:")
    print("=" * 50)
    
    print("\n✅ Expected CSV Format:")
    print("  - First row: Column headers")
    print("  - Subsequent rows: Data values")
    print("  - No empty rows between data")
    print("  - Consistent data types per column")
    
    print("\n📊 Common Column Types in Rainforest Tables:")
    print("  🌡️  Temperature: Numeric values (Fahrenheit/Celsius)")
    print("  💧 Humidity: Numeric values (0-100%)")
    print("  📊 Pressure: Numeric values (mbar, psi)")
    print("  🌪️  Flow: Numeric values (rate, velocity)")
    print("  📏 Level: Numeric values (height, depth)")
    print("  ⚡ Power: Numeric values (voltage, current)")
    print("  🕒 Timestamp: Date/time values")
    print("  🆔 ID: Unique identifiers")
    print("  📍 Status: Text values (ON/OFF, OPEN/CLOSED)")
    print("  🏷️  Tags: Text values with metadata")
    
    print("\n🔍 What the Analyzer Will Detect:")
    print("  - Column data types (numeric, text, datetime)")
    print("  - Purpose hints (temperature, humidity, etc.)")
    print("  - Data quality (null values, duplicates)")
    print("  - Relationships between tables")
    print("  - Statistical summaries")
    
    print("\n📁 File Naming Convention:")
    print("  - Use exact table names as filenames")
    print("  - Add .csv extension")
    print("  - Example: UAB2_BIO1_B4000_MISCSAV1_RFTESCOSUPTMP_327662.csv")

if __name__ == "__main__":
    print("🌿 Rainforest CSV Format Guide")
    print("=" * 40)
    
    # Create sample files
    create_sample_csv()
    
    # Show format guide
    show_csv_format_guide()
    
    # Analyze samples
    analyze_sample_files()
    
    print("\n💡 Next Steps:")
    print("1. 📁 Place your 26 CSV files in 'rainforest_tables/' directory")
    print("2. ✏️  Edit 'my_26_tables_template.py' with your table names")
    print("3. 🚀 Run the analysis to understand your tables")
    print("4. 📊 Generate comprehensive reports for your team")
