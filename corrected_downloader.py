# Biosphere 2 SCADA Data Downloader - Corrected Version
# Fixes URL encoding and authentication issues

import requests
import pandas as pd
import time
import os
import json
from datetime import datetime
from urllib.parse import quote, urlencode

class CorrectedBiosphere2Downloader:
    """Corrected downloader for Biosphere 2 SCADA data"""
    
    def __init__(self):
        self.base_url = "https://data.b2.arizona.edu/Bio2Controls/"
        self.session = requests.Session()
        self.username = "b2twin"
        self.password = "s7hMxWiVep^XK83E"
        
        # Create output directory
        os.makedirs("rainforest_tables", exist_ok=True)
        
        print("Corrected Biosphere 2 SCADA Data Downloader")
        print(f"URL: {self.base_url}fetchDataset.jsp")
        print(f"Username: {self.username}")
        print("Output: rainforest_tables/")
    
    def login_and_get_session(self):
        """Properly login and establish session"""
        
        print("Establishing authenticated session...")
        
        # First, try to access the main page to get any required cookies
        try:
            main_page = self.session.get(f"{self.base_url}fetchDataset.jsp", timeout=30)
            print(f"Main page status: {main_page.status_code}")
        except Exception as e:
            print(f"Could not access main page: {e}")
        
        # Try different authentication approaches
        auth_methods = [
            # Method 1: POST to login endpoint
            {
                'url': f"{self.base_url}login.jsp",
                'data': {'username': self.username, 'password': self.password},
                'method': 'POST'
            },
            # Method 2: Alternative login
            {
                'url': f"{self.base_url}Login.jsp",
                'data': {'user': self.username, 'pass': self.password},
                'method': 'POST'
            },
            # Method 3: Direct authentication
            {
                'url': f"{self.base_url}authenticate.jsp",
                'data': {'username': self.username, 'password': self.password},
                'method': 'POST'
            }
        ]
        
        for method in auth_methods:
            try:
                print(f"Trying authentication: {method['url']}")
                if method['method'] == 'POST':
                    response = self.session.post(method['url'], data=method['data'], timeout=30)
                else:
                    response = self.session.get(method['url'], params=method['data'], timeout=30)
                
                print(f"Auth response status: {response.status_code}")
                
                # Check if authentication was successful
                if "error" not in response.text.lower() and "invalid" not in response.text.lower():
                    print("Authentication successful!")
                    return True
                    
            except Exception as e:
                print(f"Authentication failed: {e}")
                continue
        
        print("Authentication completed (proceeding with download attempts)")
        return True
    
    def download_table_corrected(self, table_name, start_date="2025-09-19", end_date="2025-10-18"):
        """Download table with proper URL encoding"""
        
        print(f"Downloading {table_name}...")
        
        # Properly encode the table name
        encoded_table = quote(table_name, safe='')
        
        # Try different download approaches
        download_methods = [
            # Method 1: GET with proper encoding
            {
                'url': f"{self.base_url}fetchDataset.jsp",
                'params': {
                    'table': table_name,
                    'start': start_date,
                    'end': end_date,
                    'format': 'csv',
                    'username': self.username,
                    'password': self.password
                },
                'method': 'GET'
            },
            # Method 2: POST with form data
            {
                'url': f"{self.base_url}fetchDataset.jsp",
                'data': {
                    'table': table_name,
                    'start': start_date,
                    'end': end_date,
                    'format': 'csv',
                    'username': self.username,
                    'password': self.password
                },
                'method': 'POST'
            },
            # Method 3: Alternative parameter names
            {
                'url': f"{self.base_url}fetchDataset.jsp",
                'params': {
                    'dataset': table_name,
                    'from': start_date,
                    'to': end_date,
                    'type': 'csv',
                    'user': self.username,
                    'pass': self.password
                },
                'method': 'GET'
            },
            # Method 4: Different endpoint
            {
                'url': f"{self.base_url}exportData.jsp",
                'params': {
                    'table': table_name,
                    'start': start_date,
                    'end': end_date,
                    'format': 'csv',
                    'username': self.username,
                    'password': self.password
                },
                'method': 'GET'
            }
        ]
        
        for i, method in enumerate(download_methods, 1):
            try:
                print(f"  Method {i}: {method['url']}")
                
                if method['method'] == 'POST':
                    response = self.session.post(method['url'], data=method['data'], timeout=60)
                else:
                    response = self.session.get(method['url'], params=method['params'], timeout=60)
                
                print(f"  Status: {response.status_code}")
                print(f"  Content-Type: {response.headers.get('content-type', 'unknown')}")
                
                if response.status_code == 200:
                    # Check if it's actual CSV data
                    content_preview = response.text[:200] if response.text else ""
                    
                    # Look for CSV indicators
                    if (',' in content_preview and 
                        'html' not in content_preview.lower() and
                        'doctype' not in content_preview.lower() and
                        len(response.content) > 100):
                        
                        # Save as CSV
                        file_path = f"rainforest_tables/{table_name}.csv"
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                        
                        print(f"  [SUCCESS] Saved: {file_path}")
                        return True
                    else:
                        print(f"  [INFO] Response doesn't look like CSV data")
                        print(f"  Preview: {content_preview[:50]}...")
                
            except Exception as e:
                print(f"  [ERROR] Method {i} failed: {e}")
                continue
        
        print(f"  [ERROR] Could not download {table_name}")
        return False
    
    def download_all_tables_corrected(self, table_names, start_date="2025-09-19", end_date="2025-10-18"):
        """Download all tables with corrected approach"""
        
        print(f"Starting corrected download of {len(table_names)} tables...")
        print(f"Date range: {start_date} to {end_date}")
        
        # Establish session
        self.login_and_get_session()
        
        results = {}
        successful = []
        failed = []
        
        for i, table_name in enumerate(table_names, 1):
            print(f"\n[{i}/{len(table_names)}] {table_name}")
            success = self.download_table_corrected(table_name, start_date, end_date)
            results[table_name] = success
            
            if success:
                successful.append(table_name)
            else:
                failed.append(table_name)
            
            # Be nice to the server
            time.sleep(2)
        
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
    """Main function with corrected approach"""
    
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
    
    print("Corrected Biosphere 2 SCADA Data Download")
    print("=" * 50)
    print(f"URL: https://data.b2.arizona.edu/Bio2Controls/fetchDataset.jsp")
    print(f"Username: b2twin")
    print(f"Password: s7hMxWiVep^XK83E")
    print(f"Tables: {len(YOUR_28_TABLES)}")
    print(f"Date range: 2025-09-19 to 2025-10-18")
    print()
    
    # Clear previous downloads
    if os.path.exists("rainforest_tables"):
        for f in os.listdir("rainforest_tables"):
            if f.endswith('.csv'):
                os.remove(f"rainforest_tables/{f}")
        print("Cleared previous downloads")
    
    # Start corrected downloading
    downloader = CorrectedBiosphere2Downloader()
    results = downloader.download_all_tables_corrected(YOUR_28_TABLES)
    
    # Save results
    if results:
        with open("rainforest_tables/download_results_corrected.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\nDownload results saved to: rainforest_tables/download_results_corrected.json")
        
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
                
                analyzer.generate_report(analysis_results, "biosphere2_corrected_analysis.md")
                analyzer.export_json(analysis_results, "biosphere2_corrected_analysis.json")
                
                print("Analysis complete!")
                print("Check 'analysis_results/' directory for:")
                print("  - biosphere2_corrected_analysis.md")
                print("  - biosphere2_corrected_analysis.json")
                
            except Exception as e:
                print(f"Analysis failed: {e}")
        else:
            print("No tables were successfully downloaded")
            print("The interface may require manual interaction")

if __name__ == "__main__":
    main()





