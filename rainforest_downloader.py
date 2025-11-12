# Automated Rainforest Data Downloader
# Downloads 26 tables from Biosphere 2 Rainforest web interface automatically

import requests
import pandas as pd
import time
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
from urllib.parse import urljoin, urlparse
import logging

# For web scraping if needed
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False
    print("Selenium not available. Install with: pip install selenium")

class RainforestDownloader:
    """
    Automated downloader for Biosphere 2 Rainforest data
    Handles different web interface types and download patterns
    """
    
    def __init__(self, base_url: str, output_dir: str = "rainforest_tables"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.session = requests.Session()
        self.driver = None
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('rainforest_download.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        print(f"🌿 Rainforest Downloader initialized")
        print(f"📁 Output directory: {output_dir}")
        print(f"🌐 Base URL: {base_url}")
    
    def setup_selenium(self, headless: bool = True):
        """Setup Selenium WebDriver for complex web interfaces"""
        if not HAS_SELENIUM:
            self.logger.error("Selenium not available. Install with: pip install selenium")
            return False
        
        try:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Set download directory
            prefs = {
                "download.default_directory": os.path.abspath(self.output_dir),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.logger.info("✅ Selenium WebDriver initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Selenium: {e}")
            return False
    
    def detect_interface_type(self) -> str:
        """Detect the type of web interface"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            content = response.text.lower()
            
            # Common interface patterns
            if "grafana" in content:
                return "grafana"
            elif "influxdb" in content:
                return "influxdb"
            elif "prometheus" in content:
                return "prometheus"
            elif "tableau" in content:
                return "tableau"
            elif "powerbi" in content:
                return "powerbi"
            elif "custom" in content or "biosphere" in content:
                return "custom"
            else:
                return "unknown"
                
        except Exception as e:
            self.logger.error(f"❌ Failed to detect interface type: {e}")
            return "unknown"
    
    def download_via_api(self, table_names: List[str], start_date: str, end_date: str) -> Dict[str, bool]:
        """Download data via REST API"""
        self.logger.info("🔌 Attempting API download...")
        
        results = {}
        
        # Common API endpoints to try
        api_endpoints = [
            "/api/data",
            "/api/export",
            "/api/tables",
            "/api/sensors",
            "/data",
            "/export"
        ]
        
        for table_name in table_names:
            success = False
            
            for endpoint in api_endpoints:
                try:
                    # Try different API patterns
                    api_urls = [
                        f"{self.base_url}{endpoint}/{table_name}",
                        f"{self.base_url}{endpoint}?table={table_name}",
                        f"{self.base_url}{endpoint}?sensor={table_name}",
                        f"{self.base_url}{endpoint}?name={table_name}"
                    ]
                    
                    for api_url in api_urls:
                        params = {
                            "start_date": start_date,
                            "end_date": end_date,
                            "format": "csv"
                        }
                        
                        response = self.session.get(api_url, params=params, timeout=30)
                        
                        if response.status_code == 200 and "csv" in response.headers.get("content-type", ""):
                            # Save CSV file
                            file_path = os.path.join(self.output_dir, f"{table_name}.csv")
                            with open(file_path, 'wb') as f:
                                f.write(response.content)
                            
                            self.logger.info(f"✅ Downloaded {table_name} via API")
                            success = True
                            break
                    
                    if success:
                        break
                        
                except Exception as e:
                    self.logger.debug(f"API attempt failed for {table_name}: {e}")
                    continue
            
            results[table_name] = success
            
            if success:
                time.sleep(1)  # Be respectful to the server
        
        return results
    
    def download_via_selenium(self, table_names: List[str], start_date: str, end_date: str) -> Dict[str, bool]:
        """Download data using Selenium for complex web interfaces"""
        if not self.driver:
            self.logger.error("❌ Selenium driver not initialized")
            return {name: False for name in table_names}
        
        self.logger.info("🤖 Attempting Selenium download...")
        results = {}
        
        try:
            # Navigate to the main page
            self.driver.get(self.base_url)
            time.sleep(3)
            
            for table_name in table_names:
                success = False
                
                try:
                    # Common patterns for table selection
                    selectors_to_try = [
                        f"//select[contains(@name, 'table')]",
                        f"//select[contains(@id, 'table')]",
                        f"//option[contains(text(), '{table_name}')]",
                        f"//a[contains(text(), '{table_name}')]",
                        f"//button[contains(text(), '{table_name}')]",
                        f"//input[@value='{table_name}']"
                    ]
                    
                    for selector in selectors_to_try:
                        try:
                            element = self.driver.find_element(By.XPATH, selector)
                            
                            if element.tag_name == "select":
                                # Handle dropdown selection
                                from selenium.webdriver.support.ui import Select
                                select = Select(element)
                                select.select_by_visible_text(table_name)
                            elif element.tag_name == "option":
                                # Click on option
                                element.click()
                            elif element.tag_name in ["a", "button"]:
                                # Click on link/button
                                element.click()
                            elif element.tag_name == "input":
                                # Check checkbox or radio button
                                element.click()
                            
                            time.sleep(2)
                            
                            # Try to set date range
                            self._set_date_range(start_date, end_date)
                            
                            # Look for download/export button
                            download_selectors = [
                                "//button[contains(text(), 'Download')]",
                                "//button[contains(text(), 'Export')]",
                                "//a[contains(text(), 'Download')]",
                                "//a[contains(text(), 'Export')]",
                                "//input[@type='submit' and contains(@value, 'Download')]",
                                "//input[@type='submit' and contains(@value, 'Export')]"
                            ]
                            
                            for download_selector in download_selectors:
                                try:
                                    download_btn = self.driver.find_element(By.XPATH, download_selector)
                                    download_btn.click()
                                    time.sleep(5)  # Wait for download
                                    
                                    # Check if file was downloaded
                                    file_path = os.path.join(self.output_dir, f"{table_name}.csv")
                                    if os.path.exists(file_path):
                                        self.logger.info(f"✅ Downloaded {table_name} via Selenium")
                                        success = True
                                        break
                                        
                                except NoSuchElementException:
                                    continue
                            
                            if success:
                                break
                                
                        except NoSuchElementException:
                            continue
                    
                    if not success:
                        self.logger.warning(f"⚠️ Could not download {table_name} via Selenium")
                    
                except Exception as e:
                    self.logger.error(f"❌ Error downloading {table_name}: {e}")
                
                results[table_name] = success
                time.sleep(2)  # Be respectful
        
        except Exception as e:
            self.logger.error(f"❌ Selenium download failed: {e}")
            return {name: False for name in table_names}
        
        return results
    
    def _set_date_range(self, start_date: str, end_date: str):
        """Set date range in web interface"""
        try:
            # Common date input patterns
            date_selectors = [
                "//input[@type='date']",
                "//input[contains(@name, 'start')]",
                "//input[contains(@name, 'end')]",
                "//input[contains(@id, 'start')]",
                "//input[contains(@id, 'end')]"
            ]
            
            for selector in date_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if len(elements) >= 2:
                        elements[0].clear()
                        elements[0].send_keys(start_date)
                        elements[1].clear()
                        elements[1].send_keys(end_date)
                        break
                except:
                    continue
                    
        except Exception as e:
            self.logger.debug(f"Could not set date range: {e}")
    
    def download_all_tables(self, table_names: List[str], start_date: str = "2025-09-19", end_date: str = "2025-10-18") -> Dict[str, bool]:
        """
        Download all 26 tables automatically
        
        Args:
            table_names: List of your 26 table names
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Dictionary with download success status for each table
        """
        self.logger.info(f"🚀 Starting download of {len(table_names)} tables")
        self.logger.info(f"📅 Date range: {start_date} to {end_date}")
        
        # Detect interface type
        interface_type = self.detect_interface_type()
        self.logger.info(f"🔍 Detected interface type: {interface_type}")
        
        # Try API download first
        api_results = self.download_via_api(table_names, start_date, end_date)
        
        # Check which tables were successfully downloaded
        successful_downloads = sum(api_results.values())
        self.logger.info(f"✅ API downloads successful: {successful_downloads}/{len(table_names)}")
        
        # If API didn't work for all tables, try Selenium
        if successful_downloads < len(table_names):
            self.logger.info("🤖 Trying Selenium for remaining tables...")
            
            if self.setup_selenium():
                selenium_results = self.download_via_selenium(table_names, start_date, end_date)
                
                # Merge results (Selenium overwrites API results)
                for table_name, success in selenium_results.items():
                    if success:
                        api_results[table_name] = True
                
                self.driver.quit()
        
        # Final summary
        total_successful = sum(api_results.values())
        self.logger.info(f"🎉 Download complete: {total_successful}/{len(table_names)} tables downloaded")
        
        return api_results
    
    def generate_download_report(self, results: Dict[str, bool], output_file: str = "download_report.md"):
        """Generate a report of download results"""
        report = []
        report.append("# 🌿 Rainforest Data Download Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total tables: {len(results)}")
        report.append(f"Successful downloads: {sum(results.values())}")
        report.append(f"Failed downloads: {len(results) - sum(results.values())}")
        report.append("")
        
        report.append("## 📊 Download Results")
        report.append("")
        
        successful = []
        failed = []
        
        for table_name, success in results.items():
            if success:
                successful.append(table_name)
                report.append(f"✅ {table_name}")
            else:
                failed.append(table_name)
                report.append(f"❌ {table_name}")
        
        if failed:
            report.append("")
            report.append("## ❌ Failed Downloads")
            report.append("")
            for table_name in failed:
                report.append(f"- {table_name}")
        
        report.append("")
        report.append("## 💡 Next Steps")
        report.append("1. Check the 'rainforest_tables/' directory for downloaded files")
        report.append("2. Run the table analyzer on successful downloads")
        report.append("3. For failed downloads, try manual download or contact support")
        
        # Write report
        with open(os.path.join(self.output_dir, output_file), "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        
        self.logger.info(f"📄 Download report saved: {output_file}")

# Example usage
if __name__ == "__main__":
    print("🌿 Rainforest Automated Downloader")
    print("=" * 50)
    
    # Configuration
    BASE_URL = "https://your-rainforest-web-interface-url.com"  # Replace with actual URL
    OUTPUT_DIR = "rainforest_tables"
    
    # Your 26 table names (replace with actual names)
    YOUR_26_TABLES = [
        "TABLE_1", "TABLE_2", "TABLE_3",  # Replace with actual table names
        # ... add all 26 table names
    ]
    
    # Date range
    START_DATE = "2025-09-19"
    END_DATE = "2025-10-18"
    
    print("📋 Configuration:")
    print(f"  Base URL: {BASE_URL}")
    print(f"  Output Directory: {OUTPUT_DIR}")
    print(f"  Tables: {len(YOUR_26_TABLES)}")
    print(f"  Date Range: {START_DATE} to {END_DATE}")
    
    print("\n🚀 To start downloading:")
    print("1. Update BASE_URL with your actual web interface URL")
    print("2. Update YOUR_26_TABLES with your actual table names")
    print("3. Run: downloader.download_all_tables(YOUR_26_TABLES)")
    
    # Initialize downloader
    downloader = RainforestDownloader(BASE_URL, OUTPUT_DIR)
    
    # Uncomment when ready to download
    # results = downloader.download_all_tables(YOUR_26_TABLES, START_DATE, END_DATE)
    # downloader.generate_download_report(results)


