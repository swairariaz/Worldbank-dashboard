import sys
import os
sys.path.append('src')

import pandas as pd
from data_loader import load_and_transform_data
from features import engineer_features, save_features

def test_feature_engineering():
    try:
        # Load cleaned data
        print("Loading data...")
        df, mapping = load_and_transform_data('data/path.csv', handle_missing=True)
        
        # Engineer features
        print("Engineering features...")
        features = engineer_features(df, reference_year=2023)
        
        print("✅ Feature engineering successful!")
        
        # Show information about each feature set
        for name, feature_df in features.items():
            print(f"\n{name.upper()}:")
            print(f"Shape: {feature_df.shape}")
            print(f"Columns: {feature_df.columns.tolist()}")
            if name == 'main_data':
                print(f"New engineered columns: {[col for col in feature_df.columns if col not in df.columns]}")
        
        # Save features
        os.makedirs('data/processed/features', exist_ok=True)
        save_features(features, 'data/processed/features')
        print(f"\n✅ Features saved to data/processed/features/")
        
        # Show sample data
        main_data = features['main_data']
        print(f"\nSample of main data with features:")
        sample_cols = ['country', 'year', 'gdp_pc_usd', 'gdp_pc_rank', 
                      'population_rank', 'ann_income_pc_growth_pct_rolling_3yr']
        sample_cols = [col for col in sample_cols if col in main_data.columns]
        print(main_data[sample_cols].head(10))
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_feature_engineering()