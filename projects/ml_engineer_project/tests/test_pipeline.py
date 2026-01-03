"""
Tests for ML Pipeline
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from data_pipeline.data_cleaner import DataCleaner
from data_pipeline.feature_engineer import FeatureEngineer


class TestDataCleaner:
    """Test data cleaning functionality"""
    
    def test_remove_duplicates(self):
        """Test duplicate removal"""
        df = pd.DataFrame({
            'id': [1, 2, 3, 3],
            'value': [10, 20, 30, 30]
        })
        
        cleaner = DataCleaner()
        df_clean = cleaner.remove_duplicates(df)
        
        assert len(df_clean) == 3
        assert cleaner.cleaning_report['duplicates_removed'] == 1
    
    def test_handle_missing_values(self):
        """Test missing value handling"""
        df = pd.DataFrame({
            'num_col': [1, 2, np.nan, 4],
            'cat_col': ['a', 'b', np.nan, 'd']
        })
        
        cleaner = DataCleaner()
        df_clean = cleaner.handle_missing_values(df, strategy='auto')
        
        assert df_clean.isnull().sum().sum() == 0
    
    def test_handle_outliers(self):
        """Test outlier handling"""
        df = pd.DataFrame({
            'values': [1, 2, 3, 4, 5, 100]  # 100 is an outlier
        })
        
        cleaner = DataCleaner()
        df_clean = cleaner.handle_outliers(df, ['values'], method='iqr')
        
        # Outlier should be capped
        assert df_clean['values'].max() < 100


class TestFeatureEngineer:
    """Test feature engineering"""
    
    def test_tenure_features(self):
        """Test tenure feature creation"""
        df = pd.DataFrame({
            'tenure': [2, 15, 30, 50]
        })
        
        engineer = FeatureEngineer()
        df_feat = engineer.create_tenure_features(df)
        
        assert 'tenure_group' in df_feat.columns
        assert 'is_new_customer' in df_feat.columns
        assert df_feat['is_new_customer'].iloc[0] == 1  # tenure <= 6
        assert df_feat['is_new_customer'].iloc[1] == 0  # tenure > 6
    
    def test_financial_features(self):
        """Test financial feature creation"""
        df = pd.DataFrame({
            'tenure': [10, 20],
            'monthly_charges': [50.0, 80.0],
            'total_charges': [500.0, 1600.0]
        })
        
        engineer = FeatureEngineer()
        df_feat = engineer.create_financial_features(df)
        
        assert 'charges_to_tenure_ratio' in df_feat.columns
        assert 'monthly_charges_category' in df_feat.columns
    
    def test_service_features(self):
        """Test service feature creation"""
        df = pd.DataFrame({
            'online_security': ['Yes', 'No'],
            'online_backup': ['Yes', 'Yes'],
            'device_protection': ['No', 'Yes'],
            'tech_support': ['Yes', 'No'],
            'streaming_tv': ['No', 'Yes'],
            'streaming_movies': ['Yes', 'Yes']
        })
        
        engineer = FeatureEngineer()
        df_feat = engineer.create_service_features(df)
        
        assert 'num_services' in df_feat.columns
        assert df_feat['num_services'].iloc[0] == 3  # Count of 'Yes'
        assert df_feat['num_services'].iloc[1] == 4


class TestModelTraining:
    """Test model training"""
    
    def test_data_split(self):
        """Test train/val/test split"""
        from models.train import ChurnModelTrainer
        
        X = pd.DataFrame(np.random.rand(100, 5))
        y = pd.Series(np.random.randint(0, 2, 100))
        
        trainer = ChurnModelTrainer()
        X_train, X_val, X_test, y_train, y_val, y_test = trainer.split_data(X, y)
        
        # Check splits
        assert len(X_train) + len(X_val) + len(X_test) == 100
        assert len(X_train) > len(X_test)  # Train should be largest
        assert len(X_val) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
