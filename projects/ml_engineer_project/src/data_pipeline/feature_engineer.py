"""
Feature Engineering Module
Creates features for churn prediction model
"""

import pandas as pd
import numpy as np
import logging
from typing import List, Tuple
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureEngineer:
    """
    Creates and transforms features for ML model
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.column_transformer = None
        self.feature_names = []
        
    def create_tenure_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create tenure-based features
        
        Args:
            df: Input DataFrame with 'tenure' column
            
        Returns:
            DataFrame with new tenure features
        """
        df_feat = df.copy()
        
        # Tenure bins
        df_feat['tenure_group'] = pd.cut(df['tenure'], 
                                         bins=[0, 12, 24, 48, 72],
                                         labels=['0-1 year', '1-2 years', '2-4 years', '4+ years'])
        
        # Is new customer
        df_feat['is_new_customer'] = (df['tenure'] <= 6).astype(int)
        
        # Tenure squared (non-linear relationship)
        df_feat['tenure_squared'] = df['tenure'] ** 2
        
        logger.info("Created tenure-based features")
        return df_feat
        
    def create_financial_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create financial features
        
        Args:
            df: Input DataFrame with financial columns
            
        Returns:
            DataFrame with financial features
        """
        df_feat = df.copy()
        
        # Total charges per month ratio
        df_feat['charges_to_tenure_ratio'] = df['total_charges'] / (df['tenure'] + 1)
        
        # Monthly charges bins
        df_feat['monthly_charges_category'] = pd.cut(df['monthly_charges'],
                                                      bins=[0, 30, 60, 90, 150],
                                                      labels=['low', 'medium', 'high', 'very_high'])
        
        # Price change indicator
        expected_total = df['monthly_charges'] * df['tenure']
        df_feat['price_changed'] = (np.abs(df['total_charges'] - expected_total) > 100).astype(int)
        
        logger.info("Created financial features")
        return df_feat
        
    def create_service_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create service usage features
        
        Args:
            df: Input DataFrame with service columns
            
        Returns:
            DataFrame with service features
        """
        df_feat = df.copy()
        
        # Count of services used
        service_cols = ['online_security', 'online_backup', 'device_protection',
                       'tech_support', 'streaming_tv', 'streaming_movies']
        
        if all(col in df.columns for col in service_cols):
            # Count 'Yes' values
            df_feat['num_services'] = df[service_cols].apply(
                lambda x: (x == 'Yes').sum(), axis=1
            )
            
            # Has premium services
            df_feat['has_premium_services'] = (df_feat['num_services'] >= 3).astype(int)
            
            # No services at all
            df_feat['no_services'] = (df_feat['num_services'] == 0).astype(int)
        
        logger.info("Created service features")
        return df_feat
        
    def create_support_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create customer support features
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with support features
        """
        df_feat = df.copy()
        
        if 'support_calls' in df.columns and 'tenure' in df.columns:
            # Support calls per month
            df_feat['support_calls_per_month'] = df['support_calls'] / (df['tenure'] + 1)
            
            # High support indicator
            df_feat['high_support'] = (df['support_calls'] > 5).astype(int)
        
        logger.info("Created support features")
        return df_feat
        
    def create_contract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create contract-related features
        
        Args:
            df: Input DataFrame with contract information
            
        Returns:
            DataFrame with contract features
        """
        df_feat = df.copy()
        
        if 'contract' in df.columns:
            # Contract duration encoding
            contract_duration = {
                'Month-to-month': 1,
                'One year': 12,
                'Two year': 24
            }
            df_feat['contract_duration_months'] = df['contract'].map(contract_duration)
            
            # Is on flexible contract
            df_feat['is_month_to_month'] = (df['contract'] == 'Month-to-month').astype(int)
        
        logger.info("Created contract features")
        return df_feat
        
    def encode_categorical_features(self, df: pd.DataFrame, 
                                    categorical_cols: List[str],
                                    method: str = 'onehot') -> pd.DataFrame:
        """
        Encode categorical variables
        
        Args:
            df: Input DataFrame
            categorical_cols: List of categorical columns to encode
            method: 'onehot' or 'label'
            
        Returns:
            DataFrame with encoded features
        """
        df_encoded = df.copy()
        
        if method == 'onehot':
            # One-hot encoding
            df_encoded = pd.get_dummies(df_encoded, columns=categorical_cols, 
                                       drop_first=True, prefix=categorical_cols)
            logger.info(f"One-hot encoded {len(categorical_cols)} categorical features")
            
        elif method == 'label':
            # Label encoding
            for col in categorical_cols:
                if col in df_encoded.columns:
                    le = LabelEncoder()
                    df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
                    self.label_encoders[col] = le
            logger.info(f"Label encoded {len(categorical_cols)} categorical features")
        
        return df_encoded
        
    def scale_numerical_features(self, df: pd.DataFrame, 
                                 numerical_cols: List[str],
                                 fit: bool = True) -> pd.DataFrame:
        """
        Scale numerical features
        
        Args:
            df: Input DataFrame
            numerical_cols: List of numerical columns to scale
            fit: Whether to fit the scaler
            
        Returns:
            DataFrame with scaled features
        """
        df_scaled = df.copy()
        
        if fit:
            df_scaled[numerical_cols] = self.scaler.fit_transform(df[numerical_cols])
            logger.info(f"Fitted and transformed {len(numerical_cols)} numerical features")
        else:
            df_scaled[numerical_cols] = self.scaler.transform(df[numerical_cols])
            logger.info(f"Transformed {len(numerical_cols)} numerical features")
        
        return df_scaled
        
    def select_features(self, df: pd.DataFrame, 
                       feature_cols: List[str],
                       target_col: str) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Select features and target variable
        
        Args:
            df: Input DataFrame
            feature_cols: List of feature columns
            target_col: Target column name
            
        Returns:
            Tuple of (X, y)
        """
        X = df[feature_cols].copy()
        y = df[target_col].copy()
        
        logger.info(f"Selected {len(feature_cols)} features and target '{target_col}'")
        logger.info(f"Feature matrix shape: {X.shape}")
        
        return X, y
        
    def engineer_features_pipeline(self, df: pd.DataFrame, 
                                   fit: bool = True) -> pd.DataFrame:
        """
        Complete feature engineering pipeline
        
        Args:
            df: Input DataFrame
            fit: Whether to fit transformers
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("Starting feature engineering pipeline...")
        
        df_feat = df.copy()
        
        # Create all engineered features
        if 'tenure' in df.columns:
            df_feat = self.create_tenure_features(df_feat)
        
        if 'monthly_charges' in df.columns and 'total_charges' in df.columns:
            df_feat = self.create_financial_features(df_feat)
        
        df_feat = self.create_service_features(df_feat)
        df_feat = self.create_support_features(df_feat)
        df_feat = self.create_contract_features(df_feat)
        
        logger.info("Feature engineering pipeline completed")
        logger.info(f"Final feature count: {len(df_feat.columns)}")
        
        return df_feat
        
    def get_feature_importance_names(self) -> List[str]:
        """
        Get list of feature names after transformation
        
        Returns:
            List of feature names
        """
        return self.feature_names


if __name__ == "__main__":
    # Example usage
    sample_data = {
        'customer_id': [1, 2, 3, 4, 5],
        'tenure': [2, 24, 48, 6, 36],
        'monthly_charges': [50.0, 75.0, 90.0, 45.0, 80.0],
        'total_charges': [100.0, 1800.0, 4320.0, 270.0, 2880.0],
        'contract': ['Month-to-month', 'One year', 'Two year', 'Month-to-month', 'Two year'],
        'online_security': ['Yes', 'No', 'Yes', 'No', 'Yes'],
        'online_backup': ['No', 'Yes', 'Yes', 'No', 'Yes'],
        'device_protection': ['No', 'No', 'Yes', 'No', 'Yes'],
        'tech_support': ['No', 'Yes', 'Yes', 'No', 'Yes'],
        'streaming_tv': ['Yes', 'No', 'Yes', 'Yes', 'No'],
        'streaming_movies': ['No', 'Yes', 'Yes', 'No', 'Yes'],
        'support_calls': [0, 2, 1, 5, 0]
    }
    
    df = pd.DataFrame(sample_data)
    print("Original Data:")
    print(df.head())
    print()
    
    engineer = FeatureEngineer()
    df_engineered = engineer.engineer_features_pipeline(df)
    
    print("\nEngineered Features:")
    print(df_engineered.columns.tolist())
    print(df_engineered.head())
