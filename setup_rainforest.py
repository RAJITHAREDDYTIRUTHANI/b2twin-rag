# Rainforest Analysis Setup - Simple Version
# No Unicode characters to avoid encoding issues

import os
import json

def create_setup():
    """Create the complete setup for Rainforest analysis"""
    
    print("Rainforest Analysis Setup")
    print("=" * 40)
    
    # Create directories
    directories = ["rainforest_tables", "analysis_results"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created: {directory}/")
    
    # Create configuration file
    config_content = '''# Your 26 Rainforest Tables Configuration
# Fill in your details and run the analysis

# STEP 1: Your web interface URL
WEB_INTERFACE_URL = "https://your-rainforest-web-interface-url.com"

# STEP 2: Your 26 table names (replace with actual names)
YOUR_26_TABLES = [
    "TABLE_NAME_1",
    "TABLE_NAME_2", 
    "TABLE_NAME_3",
    "TABLE_NAME_4",
    "TABLE_NAME_5",
    "TABLE_NAME_6",
    "TABLE_NAME_7",
    "TABLE_NAME_8",
    "TABLE_NAME_9",
    "TABLE_NAME_10",
    "TABLE_NAME_11",
    "TABLE_NAME_12",
    "TABLE_NAME_13",
    "TABLE_NAME_14",
    "TABLE_NAME_15",
    "TABLE_NAME_16",
    "TABLE_NAME_17",
    "TABLE_NAME_18",
    "TABLE_NAME_19",
    "TABLE_NAME_20",
    "TABLE_NAME_21",
    "TABLE_NAME_22",
    "TABLE_NAME_23",
    "TABLE_NAME_24",
    "TABLE_NAME_25",
    "TABLE_NAME_26",
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
'''
    
    with open("my_rainforest_config.py", "w") as f:
        f.write(config_content)
    
    print("Created: my_rainforest_config.py")
    
    # Create simple instructions
    instructions = '''# Rainforest Analysis Instructions

## Quick Start:

1. Edit 'my_rainforest_config.py':
   - Add your web interface URL
   - Add your 26 table names
   - Verify date range (Sep 19 - Oct 18, 2025)

2. Run the analysis:
   python my_rainforest_config.py

3. Check results:
   - rainforest_tables/ (downloaded CSV files)
   - analysis_results/ (analysis reports)

## What you'll get:

- Comprehensive table analysis
- Column meaning detection
- Data quality assessment
- Table relationship mapping
- Statistical summaries

## If download fails:

- Manually download CSV files
- Place them in 'rainforest_tables/' directory
- Run the analyzer separately

## Example table names:
- UAB2_BIO1_B4000_MISCSAV1_RFTESCOSUPTMP_327662
- UAB2_BIO1_B4000_MISCSAV1_RFTESCOVFDDIRCMD_322444
- UAB2_BIO1_B4000_MISCSAV1_RFTESCOVFDOUT_317704
'''
    
    with open("INSTRUCTIONS.txt", "w") as f:
        f.write(instructions)
    
    print("Created: INSTRUCTIONS.txt")
    
    print("\nSetup complete!")
    print("Next steps:")
    print("1. Edit 'my_rainforest_config.py' with your details")
    print("2. Run: python my_rainforest_config.py")
    print("3. Check 'analysis_results/' for your reports")

if __name__ == "__main__":
    create_setup()


