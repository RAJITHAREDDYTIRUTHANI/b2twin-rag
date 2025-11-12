# Complete Rainforest Analysis Guide
# Download + Analyze your 26 Rainforest tables automatically

import os
import json
from datetime import datetime

def create_your_26_tables_template():
    """Create a template file for your 26 tables"""
    
    template_content = '''# Your 26 Rainforest Tables Configuration
# Fill in your details and run the analysis

# STEP 1: Your web interface URL
WEB_INTERFACE_URL = "https://your-rainforest-web-interface-url.com"

# STEP 2: Your 26 table names (replace with actual names)
YOUR_26_TABLES = [
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

# STEP 3: Date range for your data
START_DATE = "2025-09-19"
END_DATE = "2025-10-18"

# STEP 4: Run the complete analysis
def run_complete_analysis():
    """Run complete download and analysis"""
    
    print("🌿 Complete Rainforest Analysis")
    print("=" * 50)
    
    # Check configuration
    if WEB_INTERFACE_URL == "https://your-rainforest-web-interface-url.com":
        print("❌ Please update WEB_INTERFACE_URL with your actual URL")
        return
    
    if YOUR_26_TABLES[0] == "TABLE_NAME_1":
        print("❌ Please add your actual table names to YOUR_26_TABLES")
        return
    
    # Step 1: Download tables
    print("📥 Step 1: Downloading tables...")
    from simple_downloader import SimpleRainforestDownloader
    
    downloader = SimpleRainforestDownloader(WEB_INTERFACE_URL)
    download_results = downloader.download_all_tables(YOUR_26_TABLES, START_DATE, END_DATE)
    
    # Step 2: Analyze downloaded tables
    print("\\n🔍 Step 2: Analyzing tables...")
    from rainforest_analyzer import RainforestTableAnalyzer
    
    analyzer = RainforestTableAnalyzer()
    
    # Only analyze successfully downloaded tables
    successful_tables = [name for name, success in download_results.items() if success]
    
    if successful_tables:
        analysis_results = analyzer.analyze_multiple_tables(successful_tables)
        
        # Step 3: Generate reports
        print("\\n📊 Step 3: Generating reports...")
        analyzer.generate_analysis_report("my_26_tables_complete_analysis.md")
        analyzer.export_analysis_json("my_26_tables_complete_analysis.json")
        analyzer.create_column_dictionary("my_26_tables_column_dictionary.md")
        
        print("\\n✅ Complete analysis finished!")
        print("📁 Check 'analysis_results/' directory for:")
        print("  - my_26_tables_complete_analysis.md (comprehensive report)")
        print("  - my_26_tables_complete_analysis.json (raw data)")
        print("  - my_26_tables_column_dictionary.md (column meanings)")
    else:
        print("❌ No tables were successfully downloaded")

# Run the analysis
if __name__ == "__main__":
    run_complete_analysis()
'''
    
    with open("your_26_tables_config.py", "w") as f:
        f.write(template_content)
    
    print("✅ Created: your_26_tables_config.py")
    print("📝 Edit this file with your actual table names and URL")

def show_step_by_step_guide():
    """Show step-by-step instructions"""
    
    print("🌿 Complete Rainforest Analysis Guide")
    print("=" * 50)
    
    print("\n📋 Step-by-Step Instructions:")
    print("=" * 30)
    
    print("\n1️⃣ PREPARATION:")
    print("   - Get your web interface URL from your team")
    print("   - Get your 26 assigned table names")
    print("   - Note the date range: Sep 19, 2025 to Oct 18, 2025")
    
    print("\n2️⃣ CONFIGURATION:")
    print("   - Edit 'your_26_tables_config.py'")
    print("   - Add your web interface URL")
    print("   - Add your 26 table names")
    print("   - Verify the date range")
    
    print("\n3️⃣ DOWNLOAD:")
    print("   - Run: python your_26_tables_config.py")
    print("   - The script will automatically download all 26 tables")
    print("   - Files will be saved in 'rainforest_tables/' directory")
    
    print("\n4️⃣ ANALYSIS:")
    print("   - The script will automatically analyze downloaded tables")
    print("   - Column meanings will be detected")
    print("   - Relationships between tables will be identified")
    
    print("\n5️⃣ REPORTS:")
    print("   - Check 'analysis_results/' directory")
    print("   - Comprehensive report: my_26_tables_complete_analysis.md")
    print("   - Column dictionary: my_26_tables_column_dictionary.md")
    print("   - Raw data: my_26_tables_complete_analysis.json")
    
    print("\n💡 TIPS:")
    print("   - Table names might look like: UAB2_BIO1_B4000_MISCSAV1_RFTESCOSUPTMP_327662")
    print("   - If download fails, try manual download for those tables")
    print("   - The analyzer will work with any successfully downloaded files")
    
    print("\n🚀 QUICK START:")
    print("   1. python your_26_tables_config.py")
    print("   2. Edit the configuration file")
    print("   3. Run again to download and analyze")

def create_directory_structure():
    """Create the necessary directory structure"""
    
    directories = [
        "rainforest_tables",
        "analysis_results",
        "downloads"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("📁 Directory structure created:")
    for directory in directories:
        print(f"   {directory}/")

if __name__ == "__main__":
    print("🌿 Rainforest Complete Analysis Setup")
    print("=" * 50)
    
    # Create directories
    create_directory_structure()
    
    # Create configuration template
    create_your_26_tables_template()
    
    # Show guide
    show_step_by_step_guide()
    
    print("\n🎯 NEXT STEPS:")
    print("1. Edit 'your_26_tables_config.py' with your details")
    print("2. Run: python your_26_tables_config.py")
    print("3. Check 'analysis_results/' for your comprehensive analysis")
    
    print("\n📞 NEED HELP?")
    print("- Check the generated configuration file")
    print("- Make sure your web interface URL is correct")
    print("- Verify your table names match exactly")
    print("- The analyzer will work with any CSV files you provide")


