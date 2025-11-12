# Biosphere 2 SCADA Data - Manual Download Guide
# Clear instructions with your specific credentials

def create_manual_guide():
    """Create step-by-step manual download guide"""
    
    guide = """# Biosphere 2 SCADA Data - Manual Download Guide

## Your Credentials
- **URL**: https://data.b2.arizona.edu/Bio2Controls/fetchDataset.jsp
- **Username**: b2twin
- **Password**: s7hMxWiVep^XK83E

## Step-by-Step Instructions

### Step 1: Access the Download Interface
1. Open your web browser
2. Go to: https://data.b2.arizona.edu/Bio2Controls/fetchDataset.jsp
3. Login with your credentials:
   - Username: b2twin
   - Password: s7hMxWiVep^XK83E

### Step 2: Download Your 28 Tables
For each table below, follow these steps:

1. **Select the table** from the dropdown/list
2. **Set date range**: 
   - Start Date: 2025-09-19
   - End Date: 2025-10-18
3. **Choose format**: CSV
4. **Click Download**
5. **Save** the file with the exact table name

### Your 28 Tables to Download:

```
1. Rainforest AHUR5_EDPosSp – [%]
2. Rainforest AHUR5_EDPos – [%]
3. Rainforest AHUR4_EDCmd
4. Rainforest AHUR4_SysReset
5. Rainforest AHUR4_TWCCVlvCmd – [%]
6. Rainforest AHUR4_SFCmd
7. Rainforest AHUR4_SFAmps – Electric current [A]
8. Rainforest AHUR4_SATmpSp – Temperature [°F]
9. Rainforest AHUR4_SATmp – Temperature [°F]
10. Rainforest AHUR4_MinVlvPos – [%]
11. Rainforest AHUR4_OccCmd
12. Rainforest AHUR4_MinSATmpSp – Temperature [°F]
13. Rainforest AHUR4_MaxSATmpSp – Temperature [°F]
14. Rainforest AHUR4_FanAlm
15. Rainforest AHUR4_FanSts –
16. Rainforest AHUR4_EDPosSp – [%]
17. Rainforest AHUR4_EDPos – [%]
18. Rainforest AHUR4_EDCmd – [%]
19. Rainforest AHUR4_CCVlvCmd – [%]
20. Rainforest AHUR3_TWCCVlvCmd – [%]
21. Rainforest AHUR3_SFCmd –
22. Rainforest AHUR3_SATmp – Temperature [°F]
23. Rainforest AHUR3_SFAmps – Electric current [A]
24. Rainforest AHUR3_OccCmd –
25. Rainforest AHUR3_HCVlvCmd – [%]
26. Rainforest AHUR3_EDCmd – [%]
27. Rainforest AHUR3_EDPosSp – [%]
28. Rainforest AHUR3_EDPos – [%]
```

### Step 3: Organize Files
1. Create a folder called `rainforest_tables` in your project directory
2. Place all downloaded CSV files in this folder
3. Make sure filenames match the table names exactly

### Step 4: Run Analysis
Once you have all files downloaded:

```bash
python simple_config.py
```

Choose option 2 (manual analysis)

## Alternative: Try Automatic Download First

Before manual download, try the automatic downloader:

```bash
python biosphere2_downloader.py
```

This will attempt to download all 28 tables automatically using your credentials.

## Troubleshooting

### If automatic download fails:
- The interface might require manual interaction
- Some tables might not be available for the specified date range
- Try manual download for the tables that failed

### If manual download fails:
- Check your internet connection
- Verify the date range is valid (Sep 19 - Oct 18, 2025)
- Ensure you have permission to access the data
- Try downloading one table at a time

### If analysis fails:
- Check that CSV files are in the `rainforest_tables/` folder
- Verify filenames match exactly (including spaces and special characters)
- Ensure files are not corrupted or empty

## Expected Results

After successful download and analysis, you'll get:

1. **CSV files** in `rainforest_tables/` directory
2. **Analysis report** in `analysis_results/biosphere2_analysis.md`
3. **Raw data** in `analysis_results/biosphere2_analysis.json`

The analysis will provide:
- Column meanings and data types
- Data quality assessment
- Statistical summaries
- Table relationships
- Comprehensive documentation

## Next Steps

1. Try automatic download first: `python biosphere2_downloader.py`
2. If that fails, use manual download following this guide
3. Run analysis: `python simple_config.py` (option 2)
4. Check results in `analysis_results/` directory
5. Share findings with your team

## Quick Start Commands

```bash
# Try automatic download
python biosphere2_downloader.py

# If that fails, run manual analysis
python simple_config.py
# Choose option 2

# Check results
ls analysis_results/
```
"""
    
    with open("MANUAL_DOWNLOAD_GUIDE.md", "w") as f:
        f.write(guide)
    
    print("Created: MANUAL_DOWNLOAD_GUIDE.md")
    print("This guide contains step-by-step instructions with your credentials")

def main():
    """Create the manual download guide"""
    
    print("Biosphere 2 SCADA Data - Manual Download Guide")
    print("=" * 50)
    
    create_manual_guide()
    
    print("\nGuide created successfully!")
    print("\nNext steps:")
    print("1. Try automatic download: python biosphere2_downloader.py")
    print("2. If that fails, follow MANUAL_DOWNLOAD_GUIDE.md")
    print("3. Run analysis: python simple_config.py (option 2)")
    
    print("\nYour credentials are ready:")
    print("URL: https://data.b2.arizona.edu/Bio2Controls/fetchDataset.jsp")
    print("Username: b2twin")
    print("Password: s7hMxWiVep^XK83E")

if __name__ == "__main__":
    main()





