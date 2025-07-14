import csv
import os

def explore_csv_structure(file_path):
    """
    Explore the basic structure of a CSV file
    
    Args:
        file_path (str): Path to the CSV file to explore
        
    Returns:
        None: Prints exploration results to console
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"EXPLORING: {os.path.basename(file_path)}")
    print(f"{'='*60}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            
            headers = next(reader)
            print(f"Columns: {len(headers)}")
            print(f"Column names:")
            for i, header in enumerate(headers, 1):
                print(f"   {i:2d}. {header}")
            
            
            print(f"\nSample Data (first 3 rows):")
            sample_rows = []
            for i, row in enumerate(reader):
                if i < 3:
                    sample_rows.append(row)
                else:
                    break
            
            for i, row in enumerate(sample_rows, 1):
                print(f"\nRow {i}:")
                for j, (header, value) in enumerate(zip(headers[:5], row[:5])):  
                    print(f"   {header}: {value}")
                if len(row) > 5:
                    print(f"   ... and {len(row)-5} more columns")
        
        
        with open(file_path, 'r', encoding='utf-8') as f:
            total_rows = sum(1 for line in f) - 1  
        
        print(f"\nTotal data rows: {total_rows:,}")
        
        
        file_size = os.path.getsize(file_path) / (1024 * 1024)  
        print(f"File size: {file_size:.1f} MB")
        
    except Exception as e:
        print(f"Error reading file: {e}")

def identify_column_types(file_path):
    """
    Identify likely data types for each column
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        None: Prints column type analysis
    """
    if not os.path.exists(file_path):
        return
    
    print(f"\nColumn Type Analysis:")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            
            
            sample_rows = []
            for i, row in enumerate(reader):
                if i < 100:  
                    sample_rows.append(row)
                else:
                    break
        
        for i, header in enumerate(headers):
            
            values = [row[i] if i < len(row) else '' for row in sample_rows]
            non_empty = [v.strip() for v in values if v.strip()]
            
            if not non_empty:
                col_type = "Empty"
            elif all(v.replace(',', '').replace('.', '').replace('-', '').isdigit() for v in non_empty):
                col_type = "Numeric"
            elif len(set(non_empty)) < len(non_empty) * 0.1:  
                col_type = "Categorical"
            elif any(keyword in header.lower() for keyword in ['date', 'time', 'created']):
                col_type = "DateTime"
            else:
                col_type = "Text"
            
            unique_count = len(set(non_empty))
            print(f"   {header:30s} | {col_type:12s} | {unique_count:4d} unique values")
            
    except Exception as e:
        print(f"Error analyzing column types: {e}")

def main():
    """
    Main function to explore all dataset files
    """
    print("Election Social Media Data Explorer")
    print("===================================")
    
    
    data_files = [
        "period_03/2024_fb_posts_president_scored_anon.csv",
        "period_03/2024_fb_ads_president_scored_anon.csv", 
        "period_03/2024_tw_posts_president_scored_anon.csv"
    ]
    
    total_rows = 0
    
    for file_path in data_files:
        explore_csv_structure(file_path)
        identify_column_types(file_path)
        
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                file_rows = sum(1 for line in f) - 1
                total_rows += file_rows
    
    print(f"\n{'='*60}")
    print(f"DATASET SUMMARY")
    print(f"{'='*60}")
    print(f"Total files: {len(data_files)}")
    print(f"Total records: {total_rows:,}")
    print(f"Platforms: Facebook (posts + ads), Twitter")
    print(f"Time period: 2024 US Presidential Election")
    print(f"Ready for descriptive analysis!")

if __name__ == "__main__":
    main()