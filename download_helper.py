# Simple Biosphere 2 Download Guide
# Step-by-step instructions for manual download

import os

def create_download_instructions():
    """Create detailed download instructions"""
    
    instructions = """# Biosphere 2 SCADA Data Download Instructions

## The Issue
The download URL `https://data.b2.arizona.edu/Bio2Controls/fetchDataset.jsp` requires authentication credentials, which is why the automatic downloader fails.

## Solution: Manual Download

### Step 1: Get Your Credentials
1. Contact your team/instructor for Biosphere 2 login credentials
2. You need:
   - Username
   - Password

### Step 2: Access the Download Interface
1. Go to: https://data.b2.arizona.edu/Bio2Controls/fetchDataset.jsp
2. Login with your credentials
3. You should see a data download interface

### Step 3: Download Your 28 Tables
For each table below, follow these steps:

1. **Select the table** from the interface
2. **Set date range**: September 19, 2025 to October 18, 2025
3. **Choose format**: CSV
4. **Download** the file
5. **Save** with the exact table name

### Your 28 Tables:
```
Rainforest AHUR5_EDPosSp – [%]
Rainforest AHUR5_EDPos – [%]
Rainforest AHUR4_EDCmd
Rainforest AHUR4_SysReset
Rainforest AHUR4_TWCCVlvCmd – [%]
Rainforest AHUR4_SFCmd
Rainforest AHUR4_SFAmps – Electric current [A]
Rainforest AHUR4_SATmpSp – Temperature [°F]
Rainforest AHUR4_SATmp – Temperature [°F]
Rainforest AHUR4_MinVlvPos – [%]
Rainforest AHUR4_OccCmd
Rainforest AHUR4_MinSATmpSp – Temperature [°F]
Rainforest AHUR4_MaxSATmpSp – Temperature [°F]
Rainforest AHUR4_FanAlm
Rainforest AHUR4_FanSts –
Rainforest AHUR4_EDPosSp – [%]
Rainforest AHUR4_EDPos – [%]
Rainforest AHUR4_EDCmd – [%]
Rainforest AHUR4_CCVlvCmd – [%]
Rainforest AHUR3_TWCCVlvCmd – [%]
Rainforest AHUR3_SFCmd –
Rainforest AHUR3_SATmp – Temperature [°F]
Rainforest AHUR3_SFAmps – Electric current [A]
Rainforest AHUR3_OccCmd –
Rainforest AHUR3_HCVlvCmd – [%]
Rainforest AHUR3_EDCmd – [%]
Rainforest AHUR3_EDPosSp – [%]
Rainforest AHUR3_EDPos – [%]
```

### Step 4: Organize Files
1. Create a folder called `rainforest_tables`
2. Place all downloaded CSV files in this folder
3. Make sure filenames match the table names exactly

### Step 5: Run Analysis
Once you have the files:
```bash
python simple_config.py
```
Choose option 2 (manual analysis)

## Alternative: Use Existing Data
If you already have some CSV files from your previous work:
1. Copy them to `rainforest_tables/` folder
2. Rename them to match your table names
3. Run the analysis

## Troubleshooting

### If you can't access the download interface:
1. Check if you have the correct URL
2. Verify your credentials with your team
3. Try accessing from a different network/browser

### If downloads fail:
1. Try downloading one table at a time
2. Check if the date range is valid
3. Ensure you have permission to access the data

### If analysis fails:
1. Check that CSV files are in the correct folder
2. Verify filenames match exactly
3. Ensure files are not corrupted

## Next Steps
1. Get your Biosphere 2 credentials
2. Download your 28 tables manually
3. Run the analysis
4. Share results with your team
"""
    
    with open("DOWNLOAD_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)
    
    print("Created: DOWNLOAD_INSTRUCTIONS.md")
    print("This file contains detailed instructions for downloading your data")

def test_with_existing_data():
    """Test analysis with any existing CSV files"""
    
    print("\nChecking for existing data...")
    
    # Check different directories for CSV files
    directories_to_check = ["data", "rainforest_tables", "."]
    all_csv_files = []
    
    for directory in directories_to_check:
        if os.path.exists(directory):
            csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
            if csv_files:
                print(f"Found {len(csv_files)} CSV files in {directory}/:")
                for f in csv_files:
                    print(f"  - {f}")
                    all_csv_files.append(f"{directory}/{f}")
    
    if all_csv_files:
        print(f"\nTotal CSV files found: {len(all_csv_files)}")
        
        # Create rainforest_tables directory
        os.makedirs("rainforest_tables", exist_ok=True)
        
        # Copy files to rainforest_tables
        print("\nCopying files to rainforest_tables/...")
        for file_path in all_csv_files:
            filename = os.path.basename(file_path)
            import shutil
            shutil.copy(file_path, f"rainforest_tables/{filename}")
            print(f"Copied: {filename}")
        
        # Run analysis
        print("\nRunning analysis on existing data...")
        try:
            from simple_analyzer import SimpleRainforestAnalyzer
            analyzer = SimpleRainforestAnalyzer()
            
            table_names = [f.replace('.csv', '') for f in os.listdir("rainforest_tables") if f.endswith('.csv')]
            results = analyzer.analyze_multiple_tables(table_names)
            
            analyzer.generate_report(results, "existing_data_analysis.md")
            analyzer.export_json(results, "existing_data_analysis.json")
            
            print("Analysis complete!")
            print("Check 'analysis_results/' directory for reports")
            
        except Exception as e:
            print(f"Analysis failed: {e}")
    else:
        print("No CSV files found")
        print("You'll need to download your data manually")

def main():
    """Main function"""
    
    print("Biosphere 2 Data Download Helper")
    print("=" * 40)
    print("1. Create download instructions")
    print("2. Test with existing data")
    print("3. Both")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == "1":
        create_download_instructions()
    elif choice == "2":
        test_with_existing_data()
    elif choice == "3":
        create_download_instructions()
        test_with_existing_data()
    else:
        print("Invalid choice. Running both...")
        create_download_instructions()
        test_with_existing_data()
    
    print("\nSummary:")
    print("1. Check DOWNLOAD_INSTRUCTIONS.md for detailed steps")
    print("2. Get your Biosphere 2 credentials from your team")
    print("3. Download your 28 tables manually")
    print("4. Run analysis with: python simple_config.py")

if __name__ == "__main__":
    main()


