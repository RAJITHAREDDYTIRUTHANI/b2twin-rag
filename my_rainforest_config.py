# Your 26 Rainforest Tables Configuration
# Fill in your details and run the analysis

# STEP 1: Your web interface URL
#WEB_INTERFACE_URL = "https://data.b2.arizona.edu/Bio2Controls/DataAgreement.jsp"
WEB_INTERFACE_URL = "https://data.b2.arizona.edu/Bio2Controls/fetchDataset.jsp"
# STEP 2: Your 26 table names (replace with actual names)
YOUR_26_TABLES = [
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
    """Download and analyze your 26 tables"""
    
    print("Starting Rainforest Analysis...")
    
    # Check configuration
    if WEB_INTERFACE_URL == "https://your-rainforest-web-interface-url.com":
        print("ERROR: Please update WEB_INTERFACE_URL with your actual URL")
        return
    
    if YOUR_26_TABLES[0] == "TABLE_NAME_1":
        print("ERROR: Please add your actual table names to YOUR_26_TABLES")
        return
    
    # Download tables
    print("Step 1: Downloading tables...")
    try:
        from simple_downloader import SimpleRainforestDownloader
        downloader = SimpleRainforestDownloader(WEB_INTERFACE_URL)
        download_results = downloader.download_all_tables(YOUR_26_TABLES, START_DATE, END_DATE)
        
        successful_tables = [name for name, success in download_results.items() if success]
        print(f"Downloaded {len(successful_tables)} out of {len(YOUR_26_TABLES)} tables")
        
    except Exception as e:
        print(f"Download failed: {e}")
        print("You can manually place CSV files in 'rainforest_tables/' directory")
        successful_tables = []
    
    # Analyze tables
    if successful_tables:
        print("Step 2: Analyzing tables...")
        try:
            from rainforest_analyzer import RainforestTableAnalyzer
            analyzer = RainforestTableAnalyzer()
            analysis_results = analyzer.analyze_multiple_tables(successful_tables)
            
            print("Step 3: Generating reports...")
            analyzer.generate_analysis_report("my_26_tables_analysis.md")
            analyzer.export_analysis_json("my_26_tables_analysis.json")
            analyzer.create_column_dictionary("my_26_tables_column_dictionary.md")
            
            print("Analysis complete! Check 'analysis_results/' directory")
            
        except Exception as e:
            print(f"Analysis failed: {e}")
    else:
        print("No tables to analyze. Please check your configuration.")

if __name__ == "__main__":
    download_and_analyze()
