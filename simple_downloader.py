# Simple Rainforest Downloader
# Easy-to-use downloader for your 26 Rainforest tables

import requests
import pandas as pd
import time
import os
from datetime import datetime
import json

class SimpleRainforestDownloader:
    """Simple downloader for Rainforest web interface"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        
        # Create output directory
        os.makedirs("rainforest_tables", exist_ok=True)
        
        print(f"Simple Rainforest Downloader")
        print(f"Output: rainforest_tables/")
        print(f"URL: {base_url}")
    
    def download_table(self, table_name: str, start_date: str = "2025-09-19", end_date: str = "2025-10-18"):
        """Download a single table"""
        print(f"Downloading {table_name}...")
        
        # Common API patterns to try
        api_patterns = [
            f"{self.base_url}/api/data/{table_name}",
            f"{self.base_url}/api/export/{table_name}",
            f"{self.base_url}/data/{table_name}",
            f"{self.base_url}/export/{table_name}",
            f"{self.base_url}/api/tables/{table_name}/data",
            f"{self.base_url}/api/sensors/{table_name}",
        ]
        
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "format": "csv",
            "download": "true"
        }
        
        for api_url in api_patterns:
            try:
                print(f"  Trying: {api_url}")
                response = self.session.get(api_url, params=params, timeout=30)
                
                if response.status_code == 200:
                    # Check if it's CSV data
                    content_type = response.headers.get('content-type', '').lower()
                    if 'csv' in content_type or 'text' in content_type:
                        # Save the file
                        file_path = f"rainforest_tables/{table_name}.csv"
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                        
                        print(f"  [SUCCESS] Saved: {file_path}")
                        return True
                
            except Exception as e:
                print(f"  [ERROR] Failed: {e}")
                continue
        
        print(f"  [ERROR] Could not download {table_name}")
        return False
    
    def download_all_tables(self, table_names: list, start_date: str = "2025-09-19", end_date: str = "2025-10-18"):
        """Download all tables"""
        print(f"Starting download of {len(table_names)} tables...")
        print(f"📅 Date range: {start_date} to {end_date}")
        
        results = {}
        for i, table_name in enumerate(table_names, 1):
            print(f"\n[{i}/{len(table_names)}] {table_name}")
            success = self.download_table(table_name, start_date, end_date)
            results[table_name] = success
            
            if success:
                time.sleep(1)  # Be nice to the server
        
        # Summary
        successful = sum(results.values())
        print(f"\nDownload Summary:")
        print(f"  [SUCCESS] Successful: {successful}")
        print(f"  [ERROR] Failed: {len(table_names) - successful}")
        
        return results

# Quick start script
def quick_download():
    """Quick download function"""
    
    # STEP 1: Add your web interface URL here
    WEB_INTERFACE_URL = "https://your-rainforest-url.com"  # ← CHANGE THIS
    
    # STEP 2: Add your 26 table names here
    YOUR_26_TABLES = [
        # Add your table names here, for example:
        # "UAB2_BIO1_B4000_MISCSAV1_RFTESCOSUPTMP_327662",
        # "UAB2_BIO1_B4000_MISCSAV1_RFTESCOVFDDIRCMD_322444",
        # ... add all 26 tables
    ]
    
    # STEP 3: Set your date range
    START_DATE = "2025-09-19"
    END_DATE = "2025-10-18"
    
    print("Rainforest Quick Download")
    print("=" * 40)
    
    if WEB_INTERFACE_URL == "https://your-rainforest-url.com":
        print("[ERROR] Please update WEB_INTERFACE_URL with your actual URL")
        return
    
    if not YOUR_26_TABLES or YOUR_26_TABLES[0].startswith("#"):
        print("[ERROR] Please add your 26 table names to YOUR_26_TABLES")
        return
    
    # Start downloading
    downloader = SimpleRainforestDownloader(WEB_INTERFACE_URL)
    results = downloader.download_all_tables(YOUR_26_TABLES, START_DATE, END_DATE)
    
    # Save results
    with open("rainforest_tables/download_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nFiles saved in: rainforest_tables/")
    print(f"Results saved: rainforest_tables/download_results.json")

if __name__ == "__main__":
    print("Rainforest Downloader - Quick Start")
    print("=" * 50)
    
    print("\n📋 To use this downloader:")
    print("1. Edit this file and add your web interface URL")
    print("2. Add your 26 table names")
    print("3. Run: quick_download()")
    
    print("\nExample table names might look like:")
    print("  - UAB2_BIO1_B4000_MISCSAV1_RFTESCOSUPTMP_327662")
    print("  - UAB2_BIO1_B4000_MISCSAV1_RFTESCOVFDDIRCMD_322444")
    print("  - UAB2_BIO1_B4000_MISCSAV1_RFTESCOVFDOUT_317704")
    
    # Uncomment when ready to download
    # quick_download()
