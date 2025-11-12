# Biosphere 2 SCADA Data Download Helper
# Practical solution for finding the correct download URL

import webbrowser
import os
import time

def find_correct_download_url():
    """Help you find the correct download URL"""
    
    print("Biosphere 2 SCADA Data Download Helper")
    print("=" * 50)
    
    print("\nBased on your image, here are the steps to find the correct URL:")
    print("\n1. Go to: https://biosphere2.org/biosphere-2-scada-data")
    print("2. Look for the 'Download Utility SCADA Data' link")
    print("3. Click on it to see the actual download interface")
    print("4. Note the URL of the download page")
    
    print("\nCommon Biosphere 2 data URLs to try:")
    urls_to_try = [
        "https://biosphere2.org/biosphere-2-scada-data",
        "https://data.b2.arizona.edu/",
        "https://data.b2.arizona.edu/Bio2Controls/",
        "https://data.b2.arizona.edu/Bio2Controls/DataDownload.jsp",
        "https://data.b2.arizona.edu/Bio2Controls/DataExport.jsp",
        "https://data.b2.arizona.edu/Bio2Controls/SCADAData.jsp",
        "https://data.b2.arizona.edu/Bio2Controls/DataQuery.jsp"
    ]
    
    for i, url in enumerate(urls_to_try, 1):
        print(f"{i}. {url}")
    
    print("\nLet me open the main SCADA data page for you...")
    try:
        webbrowser.open("https://biosphere2.org/biosphere-2-scada-data")
        print("Opened browser to Biosphere 2 SCADA data page")
    except:
        print("Could not open browser automatically")
        print("Please manually go to: https://biosphere2.org/biosphere-2-scada-data")
    
    return urls_to_try

def create_manual_download_guide():
    """Create a guide for manual download"""
    
    guide_content = """# Manual Download Guide for Biosphere 2 SCADA Data

## Step 1: Find the Download Interface
1. Go to: https://biosphere2.org/biosphere-2-scada-data
2. Look for "Download Utility SCADA Data" link
3. Click on it to access the download interface
4. Note the URL of the download page

## Step 2: Download Your 28 Tables
Your table names:
- Rainforest AHUR5_EDPosSp – [%]
- Rainforest AHUR5_EDPos – [%]
- Rainforest AHUR4_EDCmd
- Rainforest AHUR4_SysReset
- Rainforest AHUR4_TWCCVlvCmd – [%]
- Rainforest AHUR4_SFCmd
- Rainforest AHUR4_SFAmps – Electric current [A]
- Rainforest AHUR4_SATmpSp – Temperature [°F]
- Rainforest AHUR4_SATmp – Temperature [°F]
- Rainforest AHUR4_MinVlvPos – [%]
- Rainforest AHUR4_OccCmd
- Rainforest AHUR4_MinSATmpSp – Temperature [°F]
- Rainforest AHUR4_MaxSATmpSp – Temperature [°F]
- Rainforest AHUR4_FanAlm
- Rainforest AHUR4_FanSts –
- Rainforest AHUR4_EDPosSp – [%]
- Rainforest AHUR4_EDPos – [%]
- Rainforest AHUR4_EDCmd – [%]
- Rainforest AHUR4_CCVlvCmd – [%]
- Rainforest AHUR3_TWCCVlvCmd – [%]
- Rainforest AHUR3_SFCmd –
- Rainforest AHUR3_SATmp – Temperature [°F]
- Rainforest AHUR3_SFAmps – Electric current [A]
- Rainforest AHUR3_OccCmd –
- Rainforest AHUR3_HCVlvCmd – [%]
- Rainforest AHUR3_EDCmd – [%]
- Rainforest AHUR3_EDPosSp – [%]
- Rainforest AHUR3_EDPos – [%]

## Step 3: Set Date Range
- Start Date: 2025-09-19
- End Date: 2025-10-18

## Step 4: Download Process
1. For each table, select it in the interface
2. Set the date range (Sep 19 - Oct 18, 2025)
3. Choose CSV format
4. Download the file
5. Save with the exact table name as filename

## Step 5: Place Files
1. Create a folder called 'rainforest_tables'
2. Place all downloaded CSV files in this folder
3. Make sure filenames match the table names exactly

## Step 6: Run Analysis
Once you have the files, run:
```bash
python simple_config.py
```
Choose option 2 (manual analysis)

## Alternative: Use Existing Data
If you already have some CSV files from your previous work:
1. Copy them to 'rainforest_tables/' folder
2. Rename them to match your table names
3. Run the analysis
"""
    
    with open("MANUAL_DOWNLOAD_GUIDE.md", "w") as f:
        f.write(guide_content)
    
    print("Created: MANUAL_DOWNLOAD_GUIDE.md")
    print("This guide will help you download your data manually")

def test_with_existing_data():
    """Test analysis with existing data if available"""
    
    print("\nTesting with existing data...")
    
    # Check if we have existing CSV files
    existing_files = []
    if os.path.exists("data"):
        existing_files = [f for f in os.listdir("data") if f.endswith('.csv')]
    
    if existing_files:
        print(f"Found {len(existing_files)} existing CSV files:")
        for f in existing_files:
            print(f"  - {f}")
        
        print("\nLet's copy these to rainforest_tables/ and analyze them...")
        
        # Create rainforest_tables directory
        os.makedirs("rainforest_tables", exist_ok=True)
        
        # Copy files
        for f in existing_files:
            import shutil
            shutil.copy(f"data/{f}", f"rainforest_tables/{f}")
            print(f"Copied: {f}")
        
        # Run analysis
        print("\nRunning analysis on existing data...")
        try:
            from simple_analyzer import SimpleRainforestAnalyzer
            analyzer = SimpleRainforestAnalyzer()
            
            table_names = [f.replace('.csv', '') for f in existing_files]
            results = analyzer.analyze_multiple_tables(table_names)
            
            analyzer.generate_report(results, "existing_data_analysis.md")
            analyzer.export_json(results, "existing_data_analysis.json")
            
            print("Analysis complete!")
            print("Check 'analysis_results/' directory for reports")
            
        except Exception as e:
            print(f"Analysis failed: {e}")
    else:
        print("No existing CSV files found in 'data/' directory")

def main():
    """Main function"""
    
    print("Biosphere 2 SCADA Data Helper")
    print("=" * 40)
    print("1. Find correct download URL")
    print("2. Create manual download guide")
    print("3. Test with existing data")
    print("4. All of the above")
    
    choice = input("\nChoose option (1-4): ").strip()
    
    if choice == "1":
        find_correct_download_url()
    elif choice == "2":
        create_manual_download_guide()
    elif choice == "3":
        test_with_existing_data()
    elif choice == "4":
        find_correct_download_url()
        create_manual_download_guide()
        test_with_existing_data()
    else:
        print("Invalid choice. Running all options...")
        find_correct_download_url()
        create_manual_download_guide()
        test_with_existing_data()
    
    print("\nNext steps:")
    print("1. Check MANUAL_DOWNLOAD_GUIDE.md for detailed instructions")
    print("2. Find the correct download URL from the Biosphere 2 website")
    print("3. Download your 28 tables manually")
    print("4. Run: python simple_config.py (choose option 2)")

if __name__ == "__main__":
    main()


