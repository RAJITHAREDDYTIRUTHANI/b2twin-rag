# Biosphere 2 Data Download - Issue Analysis and Solution
# The downloaded files contain HTML instead of CSV data

import os
import webbrowser

def analyze_download_issue():
    """Analyze what happened with the download"""
    
    print("Biosphere 2 Download Analysis")
    print("=" * 40)
    
    print("ISSUE IDENTIFIED:")
    print("The downloaded files contain HTML pages instead of CSV data.")
    print("This means the download interface requires additional steps.")
    
    print("\nWHAT HAPPENED:")
    print("1. The downloader successfully connected to the server")
    print("2. It received HTTP 200 responses")
    print("3. But the responses contained HTML pages, not CSV data")
    print("4. This suggests the interface needs form submission or different parameters")
    
    print("\nSOLUTIONS:")
    print("1. Manual Download (Recommended)")
    print("2. Enhanced Automated Download")
    print("3. Use Existing Data for Analysis")

def create_manual_solution():
    """Create manual download solution"""
    
    solution = """# Manual Download Solution for Biosphere 2 SCADA Data

## The Issue
The automatic downloader successfully connected but received HTML pages instead of CSV data. This is common with web interfaces that require form submission.

## Manual Download Steps

### Step 1: Access the Interface
1. Go to: https://data.b2.arizona.edu/Bio2Controls/fetchDataset.jsp
2. Login with:
   - Username: b2twin
   - Password: s7hMxWiVep^XK83E

### Step 2: Download Process
The interface likely has:
1. A form to select tables
2. Date range inputs
3. Format selection (CSV)
4. A submit button

For each of your 28 tables:
1. Select the table from dropdown/list
2. Set date range: 2025-09-19 to 2025-10-18
3. Choose CSV format
4. Click submit/download
5. Save the file with the exact table name

### Step 3: Alternative - Use Existing Data
If manual download is difficult, you can:
1. Use the existing CSV files from your previous work
2. Copy them to rainforest_tables/ directory
3. Run the analysis

## Quick Analysis with Existing Data
```bash
# Copy existing CSV files to rainforest_tables/
# Then run analysis
python simple_config.py
# Choose option 2
```

## Your 28 Tables (for reference):
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
"""
    
    with open("MANUAL_SOLUTION.md", "w") as f:
        f.write(solution)
    
    print("Created: MANUAL_SOLUTION.md")
    print("This contains the manual download solution")

def use_existing_data():
    """Use existing CSV data for analysis"""
    
    print("\nUsing Existing Data for Analysis")
    print("=" * 40)
    
    # Check if we have existing CSV files in the data directory
    if os.path.exists("data"):
        csv_files = [f for f in os.listdir("data") if f.endswith('.csv')]
        if csv_files:
            print(f"Found {len(csv_files)} existing CSV files in data/ directory:")
            for f in csv_files:
                print(f"  - {f}")
            
            print("\nCopying existing files to rainforest_tables/...")
            import shutil
            
            # Clear rainforest_tables directory first
            if os.path.exists("rainforest_tables"):
                for f in os.listdir("rainforest_tables"):
                    if f.endswith('.csv'):
                        os.remove(f"rainforest_tables/{f}")
            
            # Copy existing files
            for f in csv_files:
                shutil.copy(f"data/{f}", f"rainforest_tables/{f}")
                print(f"Copied: {f}")
            
            print("\nRunning analysis on existing data...")
            try:
                from simple_analyzer import SimpleRainforestAnalyzer
                analyzer = SimpleRainforestAnalyzer()
                
                table_names = [f.replace('.csv', '') for f in csv_files]
                results = analyzer.analyze_multiple_tables(table_names)
                
                analyzer.generate_report(results, "existing_data_analysis.md")
                analyzer.export_json(results, "existing_data_analysis.json")
                
                print("Analysis complete!")
                print("Check 'analysis_results/' directory for:")
                print("  - existing_data_analysis.md")
                print("  - existing_data_analysis.json")
                
            except Exception as e:
                print(f"Analysis failed: {e}")
        else:
            print("No existing CSV files found in data/ directory")
    else:
        print("No data/ directory found")

def open_download_interface():
    """Open the download interface in browser"""
    
    print("\nOpening Biosphere 2 download interface...")
    try:
        webbrowser.open("https://data.b2.arizona.edu/Bio2Controls/fetchDataset.jsp")
        print("Browser opened to download interface")
        print("Login with:")
        print("  Username: b2twin")
        print("  Password: s7hMxWiVep^XK83E")
    except:
        print("Could not open browser automatically")
        print("Please manually go to: https://data.b2.arizona.edu/Bio2Controls/fetchDataset.jsp")

def main():
    """Main function"""
    
    print("Biosphere 2 Download Issue Analysis")
    print("=" * 50)
    
    analyze_download_issue()
    
    print("\nOPTIONS:")
    print("1. Create manual download guide")
    print("2. Use existing data for analysis")
    print("3. Open download interface in browser")
    print("4. All of the above")
    
    choice = input("\nChoose option (1-4): ").strip()
    
    if choice == "1":
        create_manual_solution()
    elif choice == "2":
        use_existing_data()
    elif choice == "3":
        open_download_interface()
    elif choice == "4":
        create_manual_solution()
        use_existing_data()
        open_download_interface()
    else:
        print("Invalid choice. Running all options...")
        create_manual_solution()
        use_existing_data()
        open_download_interface()
    
    print("\nSUMMARY:")
    print("1. The automatic download got HTML pages instead of CSV data")
    print("2. Manual download is recommended")
    print("3. You can use existing data for analysis")
    print("4. Check MANUAL_SOLUTION.md for detailed steps")

if __name__ == "__main__":
    main()




