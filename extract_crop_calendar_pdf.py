"""
Extract Crop Calendar Data from PDF

This script extracts crop calendar information from the PDF file and converts it
to a structured CSV format for use in the farming advisory system.
"""

import pdfplumber
import pandas as pd
import re
import os

def extract_crop_calendar_from_pdf(pdf_path):
    """
    Extract crop calendar data from PDF file.
    """
    
    print("\n" + "="*70)
    print("📄 EXTRACTING CROP CALENDAR FROM PDF")
    print("="*70 + "\n")
    
    all_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"📖 Total pages: {len(pdf.pages)}")
        
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"\n📄 Processing page {page_num}...")
            
            # Extract text
            text = page.extract_text()
            if text:
                print(f"   ✅ Extracted {len(text)} characters")
                
            # Try to extract tables
            tables = page.extract_tables()
            if tables:
                print(f"   ✅ Found {len(tables)} table(s)")
                for table_num, table in enumerate(tables, 1):
                    print(f"      Table {table_num}: {len(table)} rows × {len(table[0]) if table else 0} columns")
                    all_data.append({
                        'page': page_num,
                        'table_num': table_num,
                        'data': table
                    })
    
    print(f"\n✅ Extracted {len(all_data)} tables from PDF")
    return all_data

def save_raw_extraction(all_data, output_dir='data/raw'):
    """
    Save raw extracted data for inspection.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to text file for review
    output_file = os.path.join(output_dir, 'crop_calendar_raw_extraction.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in all_data:
            f.write(f"\n{'='*70}\n")
            f.write(f"PAGE {item['page']} - TABLE {item['table_num']}\n")
            f.write(f"{'='*70}\n\n")
            
            for row in item['data']:
                f.write(' | '.join([str(cell) if cell else '' for cell in row]))
                f.write('\n')
    
    print(f"\n💾 Raw extraction saved to: {output_file}")
    return output_file

def parse_to_structured_format(all_data):
    """
    Parse extracted tables into structured crop calendar format.
    """
    
    print("\n" + "="*70)
    print("🔄 PARSING TO STRUCTURED FORMAT")
    print("="*70 + "\n")
    
    crop_calendar_records = []
    
    for item in all_data:
        table = item['data']
        
        # Skip empty tables
        if not table or len(table) < 2:
            continue
        
        # Try to identify header row
        headers = None
        data_start_row = 0
        
        for i, row in enumerate(table):
            # Look for common header keywords
            row_text = ' '.join([str(cell).lower() if cell else '' for cell in row])
            if any(keyword in row_text for keyword in ['crop', 'sowing', 'harvest', 'state', 'season']):
                headers = row
                data_start_row = i + 1
                break
        
        if headers:
            print(f"   Page {item['page']}, Table {item['table_num']} - Found headers: {headers}")
            
            # Process data rows
            for row in table[data_start_row:]:
                if row and any(cell for cell in row):  # Skip empty rows
                    record = {}
                    for i, cell in enumerate(row):
                        if i < len(headers) and headers[i]:
                            record[str(headers[i]).strip()] = str(cell).strip() if cell else ''
                    if record:
                        crop_calendar_records.append(record)
    
    print(f"\n✅ Parsed {len(crop_calendar_records)} crop calendar records")
    return crop_calendar_records

def convert_to_csv(records, output_file='data/processed/crop_calendar_extracted.csv'):
    """
    Convert parsed records to CSV matching the template format.
    """
    
    print("\n" + "="*70)
    print("💾 CONVERTING TO CSV")
    print("="*70 + "\n")
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    if records:
        df = pd.DataFrame(records)
        print(f"📊 DataFrame created with {len(df)} rows and {len(df.columns)} columns")
        print(f"\nColumns found: {list(df.columns)}")
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        print(f"\n✅ Saved to: {output_file}")
        
        # Show sample
        print(f"\n📋 SAMPLE DATA (first 5 rows):")
        print("="*70)
        print(df.head())
        
        return df
    else:
        print("⚠️ No records to save")
        return None

def main():
    """
    Main execution function.
    """
    
    pdf_path = 'New_Crop_Calendar_20.09.18.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file not found at {pdf_path}")
        return
    
    print(f"📂 Reading PDF: {pdf_path}")
    
    # Step 1: Extract raw data
    all_data = extract_crop_calendar_from_pdf(pdf_path)
    
    # Step 2: Save raw extraction for review
    raw_file = save_raw_extraction(all_data)
    
    # Step 3: Parse to structured format
    records = parse_to_structured_format(all_data)
    
    # Step 4: Convert to CSV
    df = convert_to_csv(records)
    
    print("\n" + "="*70)
    print("✅ EXTRACTION COMPLETE!")
    print("="*70)
    print(f"\n📁 Check these files:")
    print(f"   1. {raw_file} - Raw extraction for review")
    print(f"   2. data/processed/crop_calendar_extracted.csv - Structured CSV")
    print(f"\n💡 Next step: Review the extracted data and map to template columns")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
