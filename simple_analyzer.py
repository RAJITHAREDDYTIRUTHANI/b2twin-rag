# Simple Rainforest Analysis - No Unicode Issues
# Clean version for Windows compatibility

import os
import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Any

class SimpleRainforestAnalyzer:
    """Simple analyzer for Rainforest tables without Unicode issues"""
    
    def __init__(self, data_directory: str = "rainforest_tables"):
        self.data_directory = data_directory
        
        # Create directories
        os.makedirs("analysis_results", exist_ok=True)
        os.makedirs("rainforest_tables", exist_ok=True)
        
        print("Rainforest Table Analyzer initialized")
        print(f"Data directory: {data_directory}")
    
    def analyze_table(self, table_name: str) -> Dict[str, Any]:
        """Analyze a single table"""
        
        # Try different file extensions
        possible_files = [
            f"{self.data_directory}/{table_name}.csv",
            f"{self.data_directory}/{table_name}.txt",
            f"{self.data_directory}/{table_name}.dat"
        ]
        
        csv_file = None
        for file_path in possible_files:
            if os.path.exists(file_path):
                csv_file = file_path
                break
        
        if not csv_file:
            return {
                "table_name": table_name,
                "status": "error",
                "error": f"No data file found for {table_name}",
                "file_path": None
            }
        
        try:
            # Try different encodings
            df = None
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    df = pd.read_csv(csv_file, encoding=encoding)
                    break
                except:
                    continue
            
            if df is None:
                return {
                    "table_name": table_name,
                    "status": "error",
                    "error": f"Could not read file {csv_file}",
                    "file_path": csv_file
                }
            
            # Basic analysis
            analysis = {
                "table_name": table_name,
                "status": "success",
                "file_path": csv_file,
                "row_count": len(df),
                "column_count": len(df.columns),
                "columns": list(df.columns),
                "data_types": df.dtypes.to_dict(),
                "null_counts": df.isnull().sum().to_dict(),
                "sample_data": df.head(3).to_dict() if len(df) > 0 else {}
            }
            
            # Add numeric column analysis
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                analysis["numeric_summary"] = df[numeric_cols].describe().to_dict()
            
            print(f"Analysis complete: {len(df)} rows, {len(df.columns)} columns")
            return analysis
            
        except Exception as e:
            return {
                "table_name": table_name,
                "status": "error",
                "error": str(e),
                "file_path": csv_file
            }
    
    def analyze_multiple_tables(self, table_names: List[str]) -> Dict[str, Any]:
        """Analyze multiple tables"""
        
        print(f"Analyzing {len(table_names)} tables...")
        
        results = {}
        successful_tables = []
        failed_tables = []
        
        for table_name in table_names:
            result = self.analyze_table(table_name)
            results[table_name] = result
            
            if result["status"] == "success":
                successful_tables.append(table_name)
            else:
                failed_tables.append(table_name)
        
        # Summary
        summary = {
            "total_tables": len(table_names),
            "successful": len(successful_tables),
            "failed": len(failed_tables),
            "successful_tables": successful_tables,
            "failed_tables": failed_tables,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return {
            "summary": summary,
            "tables": results
        }
    
    def generate_report(self, analysis_results: Dict[str, Any], output_file: str = "rainforest_analysis.md"):
        """Generate analysis report"""
        
        report = []
        report.append("# Rainforest Database Analysis Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        summary = analysis_results["summary"]
        report.append("## Summary Statistics")
        report.append(f"- Total Tables: {summary['total_tables']}")
        report.append(f"- Successfully Analyzed: {summary['successful']}")
        report.append(f"- Failed: {summary['failed']}")
        report.append("")
        
        # Table details
        report.append("## Table Details")
        report.append("")
        
        for table_name, result in analysis_results["tables"].items():
            if result["status"] == "success":
                report.append(f"### {table_name}")
                report.append(f"- Rows: {result['row_count']}")
                report.append(f"- Columns: {result['column_count']}")
                report.append(f"- File: {result['file_path']}")
                report.append("")
            else:
                report.append(f"### {table_name} (ERROR)")
                report.append(f"- Error: {result['error']}")
                report.append("")
        
        # Save report
        report_path = f"analysis_results/{output_file}"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"Report saved: {report_path}")
    
    def export_json(self, analysis_results: Dict[str, Any], output_file: str = "rainforest_analysis.json"):
        """Export analysis results to JSON"""
        
        output_path = f"analysis_results/{output_file}"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, default=str)
        
        print(f"JSON export saved: {output_path}")

def run_simple_analysis():
    """Run simple analysis on available tables"""
    
    print("Simple Rainforest Analysis")
    print("=" * 40)
    
    # Check if we have any CSV files
    if not os.path.exists("rainforest_tables"):
        print("No rainforest_tables directory found")
        return
    
    csv_files = [f for f in os.listdir("rainforest_tables") if f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in rainforest_tables directory")
        print("Please place your CSV files there first")
        return
    
    print(f"Found {len(csv_files)} CSV files")
    
    # Extract table names from filenames
    table_names = [f.replace('.csv', '') for f in csv_files]
    
    # Run analysis
    analyzer = SimpleRainforestAnalyzer()
    results = analyzer.analyze_multiple_tables(table_names)
    
    # Generate reports
    analyzer.generate_report(results, "simple_rainforest_analysis.md")
    analyzer.export_json(results, "simple_rainforest_analysis.json")
    
    print("Analysis complete!")
    print("Check analysis_results/ directory for reports")

if __name__ == "__main__":
    run_simple_analysis()


