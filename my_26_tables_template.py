# Your 26 Rainforest Tables - Analysis Template
# Fill in your assigned table names and run the analysis

from rainforest_analyzer import RainforestTableAnalyzer
import os

def analyze_my_26_tables():
    """Analyze your specific 26 assigned Rainforest tables"""
    
    print("🌿 Analyzing Your 26 Rainforest Tables")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = RainforestTableAnalyzer()
    
    # YOUR 26 TABLE NAMES - Fill these in with your assigned tables
    your_26_tables = [
        # Table 1
        "TABLE_NAME_1",
        
        # Table 2  
        "TABLE_NAME_2",
        
        # Table 3
        "TABLE_NAME_3",
        
        # Table 4
        "TABLE_NAME_4",
        
        # Table 5
        "TABLE_NAME_5",
        
        # Table 6
        "TABLE_NAME_6",
        
        # Table 7
        "TABLE_NAME_7",
        
        # Table 8
        "TABLE_NAME_8",
        
        # Table 9
        "TABLE_NAME_9",
        
        # Table 10
        "TABLE_NAME_10",
        
        # Table 11
        "TABLE_NAME_11",
        
        # Table 12
        "TABLE_NAME_12",
        
        # Table 13
        "TABLE_NAME_13",
        
        # Table 14
        "TABLE_NAME_14",
        
        # Table 15
        "TABLE_NAME_15",
        
        # Table 16
        "TABLE_NAME_16",
        
        # Table 17
        "TABLE_NAME_17",
        
        # Table 18
        "TABLE_NAME_18",
        
        # Table 19
        "TABLE_NAME_19",
        
        # Table 20
        "TABLE_NAME_20",
        
        # Table 21
        "TABLE_NAME_21",
        
        # Table 22
        "TABLE_NAME_22",
        
        # Table 23
        "TABLE_NAME_23",
        
        # Table 24
        "TABLE_NAME_24",
        
        # Table 25
        "TABLE_NAME_25",
        
        # Table 26
        "TABLE_NAME_26",
    ]
    
    print(f"📋 Analyzing {len(your_26_tables)} tables...")
    
    # Check which files exist
    existing_tables = []
    missing_tables = []
    
    for table in your_26_tables:
        csv_path = f"rainforest_tables/{table}.csv"
        if os.path.exists(csv_path):
            existing_tables.append(table)
        else:
            missing_tables.append(table)
    
    print(f"✅ Found {len(existing_tables)} CSV files")
    print(f"❌ Missing {len(missing_tables)} CSV files")
    
    if missing_tables:
        print("\n📥 Missing files:")
        for table in missing_tables:
            print(f"  - {table}.csv")
        print("\nPlease place these CSV files in 'rainforest_tables/' directory")
        return
    
    # Analyze existing tables
    if existing_tables:
        print(f"\n🔍 Analyzing {len(existing_tables)} tables...")
        results = analyzer.analyze_multiple_tables(existing_tables)
        
        # Generate comprehensive reports
        print("\n📊 Generating reports...")
        analyzer.generate_analysis_report("my_26_tables_analysis.md")
        analyzer.export_analysis_json("my_26_tables_analysis.json")
        analyzer.create_column_dictionary("my_26_tables_column_dictionary.md")
        
        # Show summary
        print("\n📈 Analysis Summary:")
        total_rows = sum(analysis.get("total_rows", 0) for analysis in results.values() if "error" not in analysis)
        total_columns = sum(analysis.get("total_columns", 0) for analysis in results.values() if "error" not in analysis)
        
        print(f"  📊 Total Rows: {total_rows:,}")
        print(f"  📋 Total Columns: {total_columns}")
        print(f"  🗂️  Tables Analyzed: {len(existing_tables)}")
        
        # Show interesting findings
        print("\n🔍 Key Findings:")
        sensor_types = {}
        for table_name, analysis in results.items():
            if "error" not in analysis:
                for col_name, col_analysis in analysis["column_analysis"].items():
                    purpose = col_analysis["purpose_hint"]
                    if purpose in ["temperature", "humidity", "pressure", "flow", "level", "power"]:
                        if purpose not in sensor_types:
                            sensor_types[purpose] = []
                        sensor_types[purpose].append(f"{table_name}.{col_name}")
        
        for sensor_type, columns in sensor_types.items():
            print(f"  🌡️  {sensor_type.title()} sensors: {len(columns)} columns")
            for col in columns[:3]:  # Show first 3
                print(f"    - {col}")
            if len(columns) > 3:
                print(f"    - ... and {len(columns) - 3} more")
        
        print("\n✅ Analysis complete!")
        print("📁 Check 'analysis_results/' directory for detailed reports")

def create_sample_structure():
    """Create sample directory structure"""
    os.makedirs("rainforest_tables", exist_ok=True)
    os.makedirs("analysis_results", exist_ok=True)
    
    print("📁 Directory structure created:")
    print("  rainforest_tables/")
    print("    ├── TABLE_NAME_1.csv")
    print("    ├── TABLE_NAME_2.csv")
    print("    ├── ...")
    print("    └── TABLE_NAME_26.csv")
    print("  analysis_results/")
    print("    ├── my_26_tables_analysis.md")
    print("    ├── my_26_tables_analysis.json")
    print("    └── my_26_tables_column_dictionary.md")

if __name__ == "__main__":
    print("🌿 Rainforest Table Analysis - Your 26 Tables")
    print("=" * 50)
    
    # Create directory structure
    create_sample_structure()
    
    print("\n📋 Instructions:")
    print("1. ✏️  Edit this file and replace 'TABLE_NAME_X' with your actual table names")
    print("2. 📁 Place your 26 CSV files in 'rainforest_tables/' directory")
    print("3. 🚀 Run: analyze_my_26_tables()")
    print("4. 📊 Check 'analysis_results/' for your comprehensive analysis")
    
    print("\n💡 Example table names might look like:")
    print("  - UAB2_BIO1_B4000_MISCSAV1_RFTESCOSUPTMP_327662")
    print("  - UAB2_BIO1_B4000_MISCSAV1_RFTESCOVFDDIRCMD_322444")
    print("  - UAB2_BIO1_B4000_MISCSAV1_RFTESCOVFDOUT_317704")
    
    # Uncomment when ready to analyze
    # analyze_my_26_tables()
