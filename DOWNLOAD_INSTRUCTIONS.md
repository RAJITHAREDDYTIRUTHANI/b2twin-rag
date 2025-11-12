# Biosphere 2 SCADA Data Download Instructions

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
