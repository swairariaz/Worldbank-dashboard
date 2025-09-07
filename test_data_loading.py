import sys
import os
sys.path.append('src')

import pandas as pd
from data_loader import (load_and_transform_data, get_missing_data_stats, 
                        validate_data, save_cleaned_data)

def test_data_cleaning():
    try:
        # Load and transform data
        file_path = 'data/path.csv'
        print(f"Loading data from: {os.path.abspath(file_path)}")
        
        df, mapping = load_and_transform_data(file_path, handle_missing=True)
        
        print("✅ Data loading and cleaning successful!")
        print(f"Data shape: {df.shape}")
        print(f"Countries found: {len(df['country'].unique())}")
        print(f"ISO Codes: {df['iso_code'].unique()}")
        print(f"Years range: {df['year'].min()} - {df['year'].max()}")
        
        # Check missing data
        missing_stats = get_missing_data_stats(df)
        print("\nMissing data statistics after cleaning:")
        print(missing_stats)
        
        # Validate data
        is_valid, validation_report = validate_data(df)
        print(f"\nData validation: {'PASS' if is_valid else 'FAIL'}")
        print("Validation report:")
        print(validation_report)
        
        # Save cleaned data
        os.makedirs('data/processed', exist_ok=True)
        save_cleaned_data(df, 'data/processed/worldbank_indicators_cleaned.csv')
        print(f"\n✅ Cleaned data saved to data/processed/worldbank_indicators_cleaned.csv")
        
        # Show sample data
        print("\nSample data (first 3 rows):")
        print(df.head(3).to_string())
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_data_cleaning()