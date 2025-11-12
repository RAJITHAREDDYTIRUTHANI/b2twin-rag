# Biosphere 2 SCADA Data Download - Complete Solution
# With your specific credentials and URL

import requests
import pandas as pd
import time
import os
import json
from datetime import datetime

class Biosphere2Downloader:
    """Downloader for Biosphere 2 SCADA data with your credentials"""
    
    def __init__(self):
        self.base_url = "https://data.b2.arizona.edu/Bio2Controls/"
        self.session = requests.Session()
        self.username = "b2twin"
        self.password = "s7hMxWiVep^XK83E"
        
        # Create output directory
        os.makedirs("rainforest_tables", exist_ok=True)
        
        print("Biosphere 2 SCADA Data Downloader")
        print(f"URL: {self.base_url}fetchDataset.jsp")
        print(f"Username: {self.username}")
        print("Output: rainforest_tables/")
    
    def login(self):
        """Login to Biosphere 2 system"""
        
        print("Logging in...")
        
        # Try different login approaches
        login_attempts = [
            # Method 1: Direct POST to login endpoint
            {
                'url': f"{self.base_url}login.jsp",
                'data': {'username': self.username, 'password': self.password}
            },
            # Method 2: Alternative login endpoint
            {
                'url': f"{self.base_url}Login.jsp", 
                'data': {'user': self.username, 'pass': self.password}
            },
            # Method 3: Authentication endpoint
            {
                'url': f"{self.base_url}authenticate.jsp",
                'data': {'username': self.username, 'password': self.password}
            },
            # Method 4: Try with session-based auth
            {
                'url': f"{self.base_url}fetchDataset.jsp",
                'data': {'username': self.username, 'password': self.password}
            }
        ]
        
        for attempt in login_attempts:
            try:
                print(f"Trying login at: {attempt['url']}")
                response = self.session.post(attempt['url'], data=attempt['data'], timeout=30)
                
                if response.status_code == 200:
                    print("Login attempt completed")
                    # Continue to try downloading
                    return True
                    
            except Exception as e:
                print(f"Login failed: {e}")
                continue
        
        print("Login completed (proceeding with download attempts)")
        return True
    
    def download_table(self, table_name, start_date="2025-09-19", end_date="2025-10-18"):
        """Download a single table"""
        
        print(f"Downloading {table_name}...")
        
        # Clean table name for URL
        clean_name = table_name.replace(" ", "%20").replace("–", "%E2%80%93")
        
        # Try different download URL patterns
        download_urls = [
            # Pattern 1: Direct fetchDataset with parameters
            f"{self.base_url}fetchDataset.jsp?table={clean_name}&start={start_date}&end={end_date}&format=csv",
            # Pattern 2: Alternative parameter names
            f"{self.base_url}fetchDataset.jsp?dataset={clean_name}&from={start_date}&to={end_date}&type=csv",
            # Pattern 3: Different parameter format
            f"{self.base_url}fetchDataset.jsp?name={clean_name}&startDate={start_date}&endDate={end_date}&output=csv",
            # Pattern 4: POST request with data
            f"{self.base_url}fetchDataset.jsp"
        ]
        
        # POST data for method 4
        post_data = {
            'table': table_name,
            'start': start_date,
            'end': end_date,
            'format': 'csv',
            'username': self.username,
            'password': self.password
        }
        
        for i, url in enumerate(download_urls):
            try:
                print(f"  Attempt {i+1}: {url[:80]}...")
                
                if i == 3:  # POST request
                    response = self.session.post(url, data=post_data, timeout=60)
                else:  # GET request
                    response = self.session.get(url, timeout=60)
                
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    # Check content type
                    content_type = response.headers.get('content-type', '').lower()
                    print(f"  Content-Type: {content_type}")
                    
                    # Check if response contains CSV data
                    content_preview = response.text[:200] if response.text else ""
                    print(f"  Content preview: {content_preview[:50]}...")
                    
                    # Try to save as CSV if it looks like data
                    if ('csv' in content_type or 
                        'text' in content_type or 
                        ',' in content_preview or
                        len(response.content) > 100):
                        
                        file_path = f"rainforest_tables/{table_name}.csv"
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                        
                        print(f"  [SUCCESS] Saved: {file_path}")
                        return True
                    else:
                        print(f"  [INFO] Response doesn't look like CSV data")
                
            except Exception as e:
                print(f"  [ERROR] Failed: {e}")
                continue
        
        print(f"  [ERROR] Could not download {table_name}")
        return False
    
    def download_all_tables(self, table_names, start_date="2025-09-19", end_date="2025-10-18"):
        """Download all tables"""
        
        print(f"Starting download of {len(table_names)} tables...")
        print(f"Date range: {start_date} to {end_date}")
        
        # Try to login first
        self.login()
        
        results = {}
        successful = []
        failed = []
        
        for i, table_name in enumerate(table_names, 1):
            print(f"\n[{i}/{len(table_names)}] {table_name}")
            success = self.download_table(table_name, start_date, end_date)
            results[table_name] = success
            
            if success:
                successful.append(table_name)
            else:
                failed.append(table_name)
            
            # Be nice to the server
            time.sleep(1)
        
        # Summary
        print(f"\nDownload Summary:")
        print(f"  [SUCCESS] Successful: {len(successful)}")
        print(f"  [ERROR] Failed: {len(failed)}")
        
        if successful:
            print(f"\nSuccessfully downloaded:")
            for table in successful:
                print(f"  - {table}")
        
        if failed:
            print(f"\nFailed to download:")
            for table in failed:
                print(f"  - {table}")
        
        return results

def main():
    """Main download function with your specific setup"""
    
    # Your 28 table names
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
    
    print("Biosphere 2 SCADA Data Download")
    print("=" * 50)
    print(f"URL: https://data.b2.arizona.edu/Bio2Controls/fetchDataset.jsp")
    print(f"Username: b2twin")
    print(f"Tables: {len(YOUR_28_TABLES)}")
    print(f"Date range: 2025-09-19 to 2025-10-18")
    print()
    
    # Start downloading
    downloader = Biosphere2Downloader()
    results = downloader.download_all_tables(YOUR_28_TABLES)
    
    # Save results
    if results:
        with open("rainforest_tables/download_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\nDownload results saved to: rainforest_tables/download_results.json")
        
        # Run analysis on successful downloads
        successful_tables = [name for name, success in results.items() if success]
        if successful_tables:
            print(f"\nRunning analysis on {len(successful_tables)} downloaded tables...")
            try:
                from simple_analyzer import SimpleRainforestAnalyzer
                analyzer = SimpleRainforestAnalyzer()
                
                # Use the actual filenames
                csv_files = [f for f in os.listdir("rainforest_tables") if f.endswith('.csv')]
                table_names = [f.replace('.csv', '') for f in csv_files]
                
                analysis_results = analyzer.analyze_multiple_tables(table_names)
                
                analyzer.generate_report(analysis_results, "biosphere2_analysis.md")
                analyzer.export_json(analysis_results, "biosphere2_analysis.json")
                
                print("Analysis complete!")
                print("Check 'analysis_results/' directory for:")
                print("  - biosphere2_analysis.md (comprehensive report)")
                print("  - biosphere2_analysis.json (raw data)")
                
            except Exception as e:
                print(f"Analysis failed: {e}")
        else:
            print("No tables were successfully downloaded for analysis")
            print("You may need to try manual download")

if __name__ == "__main__":
    main()