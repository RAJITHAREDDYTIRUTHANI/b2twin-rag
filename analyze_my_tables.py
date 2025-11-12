# Quick Start Script for Rainforest Table Analysis
# Easy way to analyze your 26 assigned tables

from rainforest_analyzer import RainforestTableAnalyzer
import os

def analyze_your_tables():
    """Analyze your 26 assigned Rainforest tables"""
    
    print("🌿 Rainforest Table Analysis - Quick Start")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = RainforestTableAnalyzer()
    
    # STEP 1: List your 26 table names here
    # Replace these with your actual table names
    your_26_tables = [
        # Add your 26 table names here
        # Example:
        # "UAB2_BIO1_B4000_MISCSAV1_RFTESCOSUPTMP_327662",
        # "UAB2_BIO1_B4000_MISCSAV1_RFTESCOVFDDIRCMD_322444",
        # ... add all 26 tables
    ]
    
    print("📋 Your 26 Tables:")
    for i, table in enumerate(your_26_tables, 1):
        print(f"  {i:2d}. {table}")
    
    if not your_26_tables:
        print("\n⚠️  Please add your 26 table names to the 'your_26_tables' list")
        print("📝 Edit this script and add your table names")
        return
    
    # STEP 2: Check if CSV files exist
    print(f"\n📁 Checking for CSV files...")
    missing_files = []
    existing_files = []
    
    for table in your_26_tables:
        csv_file = f"rainforest_tables/{table}.csv"
        if os.path.exists(csv_file):
            existing_files.append(table)
            print(f"  ✅ {table}.csv")
        else:
            missing_files.append(table)
            print(f"  ❌ {table}.csv (missing)")
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} CSV files:")
        for table in missing_files:
            print(f"  - {table}.csv")
        print("\n📥 Please place your CSV files in the 'rainforest_tables/' directory")
        return
    
    # STEP 3: Analyze tables
    print(f"\n🔍 Analyzing {len(existing_files)} tables...")
    results = analyzer.analyze_multiple_tables(existing_files)
    
    # STEP 4: Generate reports
    print("\n📊 Generating analysis reports...")
    analyzer.generate_analysis_report("your_26_tables_analysis.md")
    analyzer.export_analysis_json("your_26_tables_analysis.json")
    analyzer.create_column_dictionary("your_26_tables_column_dictionary.md")
    
    # STEP 5: Summary
    print("\n📈 Analysis Summary:")
    total_rows = sum(analysis.get("total_rows", 0) for analysis in results.values() if "error" not in analysis)
    total_columns = sum(analysis.get("total_columns", 0) for analysis in results.values() if "error" not in analysis)
    
    print(f"  📊 Total Rows: {total_rows:,}")
    print(f"  📋 Total Columns: {total_columns}")
    print(f"  🗂️  Tables Analyzed: {len(existing_files)}")
    
    # Show some interesting findings
    print("\n🔍 Interesting Findings:")
    for table_name, analysis in results.items():
        if "error" not in analysis:
            # Find columns with interesting patterns
            interesting_cols = []
            for col_name, col_analysis in analysis["column_analysis"].items():
                if col_analysis["purpose_hint"] in ["temperature", "humidity", "pressure", "flow"]:
                    interesting_cols.append(f"{col_name} ({col_analysis['purpose_hint']})")
            
            if interesting_cols:
                print(f"  🌡️  {table_name}: {', '.join(interesting_cols)}")
    
    print("\n✅ Analysis complete!")
    print("📁 Check the 'analysis_results/' directory for detailed reports:")
    print("  - your_26_tables_analysis.md (comprehensive report)")
    print("  - your_26_tables_analysis.json (raw data)")
    print("  - your_26_tables_column_dictionary.md (column meanings)")

def setup_directories():
    """Create necessary directories"""
    os.makedirs("rainforest_tables", exist_ok=True)
    os.makedirs("analysis_results", exist_ok=True)
    print("📁 Directories created:")
    print("  - rainforest_tables/ (place your CSV files here)")
    print("  - analysis_results/ (analysis reports will be saved here)")

def show_instructions():
    """Show step-by-step instructions"""
    print("\n📋 Step-by-Step Instructions:")
    print("=" * 30)
    print("1. 📁 Place your 26 CSV files in 'rainforest_tables/' directory")
    print("2. ✏️  Edit this script and add your table names to 'your_26_tables' list")
    print("3. 🚀 Run: python analyze_my_tables.py")
    print("4. 📊 Check 'analysis_results/' for your reports")
    print("")
    print("💡 Tips:")
    print("  - CSV files should be named exactly like your table names")
    print("  - The analyzer will detect column purposes automatically")
    print("  - Reports include column meanings, data quality, and relationships")

if __name__ == "__main__":
    print("🌿 Rainforest Table Analysis - Your 26 Tables")
    print("=" * 50)
    
    # Setup directories
    setup_directories()
    
    # Show instructions
    show_instructions()
    
    # Ask if user wants to proceed
    print("\n❓ Ready to analyze your tables?")
    print("1. First, add your table names to the script")
    print("2. Place CSV files in 'rainforest_tables/' directory")
    print("3. Then run: analyze_your_tables()")
    
    # Uncomment the line below when you're ready to analyze
    # analyze_your_tables()
