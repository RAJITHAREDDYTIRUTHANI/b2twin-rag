# Rainforest Database Table Analysis Tool
# Comprehensive analysis of Biosphere 2 Rainforest environmental monitoring tables

import pandas as pd
import json
import os
from typing import Dict, List, Any, Tuple
from datetime import datetime
import sqlite3

class RainforestTableAnalyzer:
    """
    Comprehensive analyzer for Rainforest database tables
    Helps understand column meanings, data types, and relationships
    """
    
    def __init__(self, data_directory: str = "rainforest_tables"):
        self.data_directory = data_directory
        self.tables_analysis = {}
        self.column_dictionary = {}
        self.table_relationships = {}
        
        # Create output directory
        os.makedirs("analysis_results", exist_ok=True)
        os.makedirs("rainforest_tables", exist_ok=True)
        
        print("Rainforest Table Analyzer initialized")
        print(f"Data directory: {data_directory}")
    
    def analyze_table(self, table_name: str, csv_file_path: str = None) -> Dict[str, Any]:
        """
        Analyze a single Rainforest table
        
        Args:
            table_name: Name of the table
            csv_file_path: Path to CSV file (optional)
            
        Returns:
            Dictionary containing comprehensive table analysis
        """
        print(f"\n🔍 Analyzing table: {table_name}")
        
        try:
            # Load data
            if csv_file_path and os.path.exists(csv_file_path):
                df = pd.read_csv(csv_file_path)
            else:
                # Try to find CSV file in data directory
                csv_file = os.path.join(self.data_directory, f"{table_name}.csv")
                if os.path.exists(csv_file):
                    df = pd.read_csv(csv_file)
                else:
                    print(f"❌ No data file found for {table_name}")
                    return {"error": "No data file found"}
            
            # Basic table info
            analysis = {
                "table_name": table_name,
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "columns": list(df.columns),
                "data_types": df.dtypes.to_dict(),
                "memory_usage": df.memory_usage(deep=True).sum(),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            # Column analysis
            column_analysis = {}
            for col in df.columns:
                col_info = self._analyze_column(df, col)
                column_analysis[col] = col_info
            
            analysis["column_analysis"] = column_analysis
            
            # Data quality analysis
            analysis["data_quality"] = self._analyze_data_quality(df)
            
            # Sample data
            analysis["sample_data"] = df.head(5).to_dict('records')
            
            # Statistical summary for numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                analysis["statistical_summary"] = df[numeric_cols].describe().to_dict()
            
            # Store analysis
            self.tables_analysis[table_name] = analysis
            
            print(f"✅ Analysis complete: {len(df)} rows, {len(df.columns)} columns")
            return analysis
            
        except Exception as e:
            print(f"❌ Error analyzing {table_name}: {e}")
            return {"error": str(e)}
    
    def _analyze_column(self, df: pd.DataFrame, column_name: str) -> Dict[str, Any]:
        """Analyze individual column characteristics"""
        col_data = df[column_name]
        
        analysis = {
            "data_type": str(col_data.dtype),
            "non_null_count": col_data.count(),
            "null_count": col_data.isnull().sum(),
            "unique_values": col_data.nunique(),
            "null_percentage": (col_data.isnull().sum() / len(col_data)) * 100
        }
        
        # Analyze based on data type
        if col_data.dtype in ['int64', 'float64']:
            analysis.update({
                "min_value": col_data.min(),
                "max_value": col_data.max(),
                "mean_value": col_data.mean(),
                "std_value": col_data.std(),
                "column_type": "numeric"
            })
        elif col_data.dtype == 'object':
            analysis.update({
                "most_common_value": col_data.mode().iloc[0] if not col_data.mode().empty else None,
                "most_common_count": col_data.value_counts().iloc[0] if not col_data.empty else 0,
                "column_type": "text"
            })
        elif col_data.dtype == 'datetime64[ns]':
            analysis.update({
                "earliest_date": col_data.min(),
                "latest_date": col_data.max(),
                "column_type": "datetime"
            })
        
        # Detect potential column purpose
        analysis["purpose_hint"] = self._detect_column_purpose(column_name, col_data)
        
        return analysis
    
    def _detect_column_purpose(self, column_name: str, col_data: pd.Series) -> str:
        """Detect the likely purpose of a column based on name and data"""
        col_name_lower = column_name.lower()
        
        # Common Biosphere 2 sensor patterns
        purpose_hints = {
            "timestamp": ["time", "date", "timestamp", "datetime"],
            "sensor_id": ["id", "sensor_id", "device_id", "node_id"],
            "sensor_value": ["value", "reading", "measurement", "data"],
            "sensor_status": ["status", "state", "flag", "condition"],
            "sensor_type": ["type", "sensor_type", "measurement_type"],
            "location": ["location", "position", "site", "zone", "area"],
            "units": ["unit", "units", "measurement_unit"],
            "quality": ["quality", "confidence", "accuracy", "precision"],
            "temperature": ["temp", "temperature", "thermal"],
            "humidity": ["humid", "moisture", "rh"],
            "pressure": ["pressure", "barometric", "atm"],
            "flow": ["flow", "rate", "velocity", "speed"],
            "level": ["level", "height", "depth", "elevation"],
            "power": ["power", "voltage", "current", "watt"],
            "control": ["control", "command", "setpoint", "target"]
        }
        
        for purpose, keywords in purpose_hints.items():
            if any(keyword in col_name_lower for keyword in keywords):
                return purpose
        
        # Analyze data patterns
        if col_data.dtype in ['int64', 'float64']:
            if col_data.min() >= 0 and col_data.max() <= 100:
                return "percentage_or_ratio"
            elif col_data.min() >= -50 and col_data.max() <= 150:
                return "temperature_like"
            else:
                return "numeric_measurement"
        elif col_data.dtype == 'object':
            unique_vals = col_data.nunique()
            if unique_vals <= 10:
                return "categorical_status"
            else:
                return "text_data"
        
        return "unknown"
    
    def _analyze_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze overall data quality"""
        total_cells = df.shape[0] * df.shape[1]
        null_cells = df.isnull().sum().sum()
        
        return {
            "completeness_percentage": ((total_cells - null_cells) / total_cells) * 100,
            "total_null_cells": null_cells,
            "columns_with_nulls": df.columns[df.isnull().any()].tolist(),
            "duplicate_rows": df.duplicated().sum(),
            "data_freshness": self._check_data_freshness(df)
        }
    
    def _check_data_freshness(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check how recent the data is"""
        timestamp_cols = df.select_dtypes(include=['datetime64[ns]']).columns
        
        if len(timestamp_cols) > 0:
            latest_date = df[timestamp_cols[0]].max()
            earliest_date = df[timestamp_cols[0]].min()
            
            return {
                "has_timestamps": True,
                "latest_date": str(latest_date),
                "earliest_date": str(earliest_date),
                "date_range_days": (latest_date - earliest_date).days
            }
        else:
            return {"has_timestamps": False}
    
    def analyze_multiple_tables(self, table_list: List[str]) -> Dict[str, Any]:
        """Analyze multiple tables and find relationships"""
        print(f"\n🔍 Analyzing {len(table_list)} tables...")
        
        results = {}
        for table_name in table_list:
            results[table_name] = self.analyze_table(table_name)
        
        # Find relationships between tables
        self._find_table_relationships(results)
        
        return results
    
    def _find_table_relationships(self, analysis_results: Dict[str, Any]):
        """Find potential relationships between tables"""
        print("\n🔗 Analyzing table relationships...")
        
        relationships = {}
        
        # Look for common column names
        all_columns = {}
        for table_name, analysis in analysis_results.items():
            if "error" not in analysis:
                all_columns[table_name] = analysis["columns"]
        
        # Find common columns
        for table1, cols1 in all_columns.items():
            for table2, cols2 in all_columns.items():
                if table1 != table2:
                    common_cols = set(cols1) & set(cols2)
                    if common_cols:
                        relationships[f"{table1}_to_{table2}"] = {
                            "common_columns": list(common_cols),
                            "relationship_type": "shared_columns"
                        }
        
        self.table_relationships = relationships
        print(f"✅ Found {len(relationships)} potential relationships")
    
    def generate_analysis_report(self, output_file: str = "rainforest_analysis_report.md"):
        """Generate comprehensive analysis report"""
        print(f"\n📊 Generating analysis report: {output_file}")
        
        report = []
        report.append("# 🌿 Rainforest Database Analysis Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total tables analyzed: {len(self.tables_analysis)}")
        report.append("")
        
        # Summary statistics
        report.append("## 📈 Summary Statistics")
        total_rows = sum(analysis.get("total_rows", 0) for analysis in self.tables_analysis.values() if "error" not in analysis)
        total_columns = sum(analysis.get("total_columns", 0) for analysis in self.tables_analysis.values() if "error" not in analysis)
        
        report.append(f"- **Total Rows**: {total_rows:,}")
        report.append(f"- **Total Columns**: {total_columns}")
        report.append(f"- **Tables Analyzed**: {len(self.tables_analysis)}")
        report.append("")
        
        # Table details
        report.append("## 📋 Table Details")
        for table_name, analysis in self.tables_analysis.items():
            if "error" in analysis:
                report.append(f"### ❌ {table_name}")
                report.append(f"**Error**: {analysis['error']}")
                report.append("")
                continue
            
            report.append(f"### ✅ {table_name}")
            report.append(f"- **Rows**: {analysis['total_rows']:,}")
            report.append(f"- **Columns**: {analysis['total_columns']}")
            report.append(f"- **Memory Usage**: {analysis['memory_usage']:,} bytes")
            report.append("")
            
            # Column analysis
            report.append("#### Column Analysis")
            for col_name, col_analysis in analysis["column_analysis"].items():
                report.append(f"- **{col_name}** ({col_analysis['data_type']})")
                report.append(f"  - Purpose: {col_analysis['purpose_hint']}")
                report.append(f"  - Non-null: {col_analysis['non_null_count']:,}")
                report.append(f"  - Unique values: {col_analysis['unique_values']:,}")
                if col_analysis['column_type'] == 'numeric':
                    report.append(f"  - Range: {col_analysis['min_value']} to {col_analysis['max_value']}")
                report.append("")
        
        # Relationships
        if self.table_relationships:
            report.append("## 🔗 Table Relationships")
            for rel_name, rel_info in self.table_relationships.items():
                report.append(f"### {rel_name}")
                report.append(f"- **Common Columns**: {', '.join(rel_info['common_columns'])}")
                report.append(f"- **Type**: {rel_info['relationship_type']}")
                report.append("")
        
        # Recommendations
        report.append("## 💡 Analysis Recommendations")
        report.append("1. **Data Quality**: Check tables with high null percentages")
        report.append("2. **Relationships**: Use common columns to join related tables")
        report.append("3. **Performance**: Consider indexing on frequently queried columns")
        report.append("4. **Documentation**: Update column names to be more descriptive")
        report.append("")
        
        # Write report
        with open(os.path.join("analysis_results", output_file), "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        
        print(f"✅ Report saved: analysis_results/{output_file}")
    
    def export_analysis_json(self, output_file: str = "rainforest_analysis.json"):
        """Export analysis results as JSON"""
        output_path = os.path.join("analysis_results", output_file)
        
        export_data = {
            "analysis_timestamp": datetime.now().isoformat(),
            "tables_analysis": self.tables_analysis,
            "table_relationships": self.table_relationships,
            "summary": {
                "total_tables": len(self.tables_analysis),
                "total_rows": sum(analysis.get("total_rows", 0) for analysis in self.tables_analysis.values() if "error" not in analysis),
                "total_columns": sum(analysis.get("total_columns", 0) for analysis in self.tables_analysis.values() if "error" not in analysis)
            }
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, default=str)
        
        print(f"✅ JSON export saved: {output_path}")
    
    def create_column_dictionary(self, output_file: str = "column_dictionary.md"):
        """Create a comprehensive column dictionary"""
        print(f"\n📚 Creating column dictionary: {output_file}")
        
        dictionary = []
        dictionary.append("# 📚 Rainforest Database Column Dictionary")
        dictionary.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        dictionary.append("")
        
        # Group columns by purpose
        purpose_groups = {}
        for table_name, analysis in self.tables_analysis.items():
            if "error" in analysis:
                continue
            
            for col_name, col_analysis in analysis["column_analysis"].items():
                purpose = col_analysis["purpose_hint"]
                if purpose not in purpose_groups:
                    purpose_groups[purpose] = []
                
                purpose_groups[purpose].append({
                    "table": table_name,
                    "column": col_name,
                    "data_type": col_analysis["data_type"],
                    "description": f"Found in {table_name} table"
                })
        
        # Write dictionary by purpose
        for purpose, columns in purpose_groups.items():
            dictionary.append(f"## {purpose.replace('_', ' ').title()}")
            dictionary.append("")
            
            for col_info in columns:
                dictionary.append(f"### {col_info['column']}")
                dictionary.append(f"- **Table**: {col_info['table']}")
                dictionary.append(f"- **Data Type**: {col_info['data_type']}")
                dictionary.append(f"- **Description**: {col_info['description']}")
                dictionary.append("")
        
        # Write dictionary
        with open(os.path.join("analysis_results", output_file), "w", encoding="utf-8") as f:
            f.write("\n".join(dictionary))
        
        print(f"✅ Column dictionary saved: analysis_results/{output_file}")

# Example usage and testing
if __name__ == "__main__":
    print("🌿 Rainforest Table Analyzer - Test Mode")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = RainforestTableAnalyzer()
    
    # Example: Analyze your 26 tables
    # Replace with your actual table names
    your_26_tables = [
        "table_1", "table_2", "table_3",  # Replace with actual table names
        # ... add all 26 table names here
    ]
    
    print(f"📋 Example analysis for {len(your_26_tables)} tables")
    print("To analyze your actual tables:")
    print("1. Place CSV files in 'rainforest_tables/' directory")
    print("2. Update the table names list")
    print("3. Run: analyzer.analyze_multiple_tables(your_26_tables)")
    print("4. Generate reports: analyzer.generate_analysis_report()")
    
    print("\n✅ Rainforest Table Analyzer ready!")
    print("📁 Place your CSV files in 'rainforest_tables/' directory")
    print("🔍 Run analysis with your actual table names")
