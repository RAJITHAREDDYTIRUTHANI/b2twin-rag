# Simple Rainforest Configuration - No Unicode Issues
# Clean version for Windows compatibility

import os

# STEP 1: Your web interface URL
WEB_INTERFACE_URL = "https://data.b2.arizona.edu/Bio2Controls/DataAgreement.jsp"

# STEP 2: Your 28 table names (properly formatted)
YOUR_28_TABLES = [
    "Rainforest AHUR5_EDPosSp – [%]",
    "Rainforest AHUR5_EDPos – [%]",
    "Rainforest AHUR4_EDCmd",
    "Rainforest AHUR4_SysReset",
    "Rainforest AHUR4_TWCCVlvCmd – [%]",
    "Rainforest AHUR4_SFCmd",
    "Rainforest AHUR4_SFAmps – Electric current [A]",
    "Rainforest AHUR4_SATmpSp – Temperature [°F]",
    "Rainforest AHUR4_SATmp – Temperature [°F]",
    "Rainforest AHUR4_MinVlvPos – [%]",
    "Rainforest AHUR4_OccCmd",
    "Rainforest AHUR4_MinSATmpSp – Temperature [°F]",
    "Rainforest AHUR4_MaxSATmpSp – Temperature [°F]",
    "Rainforest AHUR4_FanAlm",
    "Rainforest AHUR4_FanSts –",
    "Rainforest AHUR4_EDPosSp – [%]",
    "Rainforest AHUR4_EDPos – [%]",
    "Rainforest AHUR4_EDCmd – [%]",
    "Rainforest AHUR4_CCVlvCmd – [%]",
    "Rainforest AHUR3_TWCCVlvCmd – [%]",
    "Rainforest AHUR3_SFCmd –",
    "Rainforest AHUR3_SATmp – Temperature [°F]",
    "Rainforest AHUR3_SFAmps – Electric current [A]",
    "Rainforest AHUR3_OccCmd –",
    "Rainforest AHUR3_HCVlvCmd – [%]",
    "Rainforest AHUR3_EDCmd – [%]",
    "Rainforest AHUR3_EDPosSp – [%]",
    "Rainforest AHUR3_EDPos – [%]",
]

# STEP 3: Date range
START_DATE = "2025-09-19"
END_DATE = "2025-10-18"

def download_and_analyze():
    """Download and analyze your 28 tables"""
    
    print("Starting Simple Rainforest Analysis...")
    print("=" * 50)
    
    # Check configuration
    if WEB_INTERFACE_URL == "https://your-rainforest-web-interface-url.com":
        print("ERROR: Please update WEB_INTERFACE_URL with your actual URL")
        return
    
    if YOUR_28_TABLES[0] == "TABLE_NAME_1":
        print("ERROR: Please add your actual table names to YOUR_28_TABLES")
        return
    
    print(f"Web Interface: {WEB_INTERFACE_URL}")
    print(f"Tables to analyze: {len(YOUR_28_TABLES)}")
    print(f"Date range: {START_DATE} to {END_DATE}")
    print()
    
    # Step 1: Try to download tables
    print("Step 1: Attempting to download tables...")
    try:
        from simple_downloader import SimpleRainforestDownloader
        downloader = SimpleRainforestDownloader(WEB_INTERFACE_URL)
        download_results = downloader.download_all_tables(YOUR_28_TABLES, START_DATE, END_DATE)
        
        successful_tables = [name for name, success in download_results.items() if success]
        print(f"Downloaded {len(successful_tables)} out of {len(YOUR_28_TABLES)} tables")
        
    except Exception as e:
        print(f"Download failed: {e}")
        print("You can manually place CSV files in 'rainforest_tables/' directory")
        successful_tables = []
    
    # Step 2: Analyze available tables
    print("\nStep 2: Analyzing available tables...")
    
    # Check what files we have
    if os.path.exists("rainforest_tables"):
        csv_files = [f for f in os.listdir("rainforest_tables") if f.endswith('.csv')]
        if csv_files:
            print(f"Found {len(csv_files)} CSV files in rainforest_tables/")
            
            # Use simple analyzer
            try:
                from simple_analyzer import SimpleRainforestAnalyzer
                analyzer = SimpleRainforestAnalyzer()
                
                # Extract table names from filenames
                table_names = [f.replace('.csv', '') for f in csv_files]
                results = analyzer.analyze_multiple_tables(table_names)
                
                print("\nStep 3: Generating reports...")
                analyzer.generate_report(results, "my_28_tables_analysis.md")
                analyzer.export_json(results, "my_28_tables_analysis.json")
                
                print("\nAnalysis complete!")
                print("Check 'analysis_results/' directory for:")
                print("- my_28_tables_analysis.md (comprehensive report)")
                print("- my_28_tables_analysis.json (raw data)")
                
            except Exception as e:
                print(f"Analysis failed: {e}")
        else:
            print("No CSV files found in rainforest_tables/ directory")
            print("Please manually download your tables and place them there")
    else:
        print("No rainforest_tables directory found")
        print("Creating directory...")
        os.makedirs("rainforest_tables", exist_ok=True)
        print("Please manually download your tables and place them in 'rainforest_tables/' directory")

def manual_analysis():
    """Run analysis on manually placed CSV files"""
    
    print("Manual Analysis Mode")
    print("=" * 30)
    
    if not os.path.exists("rainforest_tables"):
        print("Creating rainforest_tables directory...")
        os.makedirs("rainforest_tables", exist_ok=True)
    
    csv_files = [f for f in os.listdir("rainforest_tables") if f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found!")
        print("Please place your CSV files in 'rainforest_tables/' directory")
        return
    
    print(f"Found {len(csv_files)} CSV files:")
    for f in csv_files:
        print(f"  - {f}")
    
    # Run analysis
    from simple_analyzer import SimpleRainforestAnalyzer
    analyzer = SimpleRainforestAnalyzer()
    
    table_names = [f.replace('.csv', '') for f in csv_files]
    results = analyzer.analyze_multiple_tables(table_names)
    
    analyzer.generate_report(results, "manual_rainforest_analysis.md")
    analyzer.export_json(results, "manual_rainforest_analysis.json")
    
    print("\nManual analysis complete!")
    print("Check 'analysis_results/' directory for reports")

if __name__ == "__main__":
    print("Simple Rainforest Analysis")
    print("=" * 40)
    print("1. Try automatic download and analysis")
    print("2. Run analysis on manually placed files")
    print()
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        download_and_analyze()
    elif choice == "2":
        manual_analysis()
    else:
        print("Invalid choice. Running automatic analysis...")
        download_and_analyze()


