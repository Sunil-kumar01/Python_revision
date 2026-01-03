"""
Data Cleaning Module
Handles missing values, outliers, duplicates, and data quality issues
"""

import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCleaner:
    """
    Cleans and preprocesses raw customer data
    """
    
    def __init__(self):
        self.cleaning_report = {}
        
    def remove_duplicates(self, df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """
        Remove duplicate rows
        
        Args:
            df: Input DataFrame
            subset: Columns to consider for identifying duplicates
            
        Returns:
            DataFrame without duplicates
        """
        initial_count = len(df)
        df_clean = df.drop_duplicates(subset=subset, keep='first')
        removed = initial_count - len(df_clean)
        
        self.cleaning_report['duplicates_removed'] = removed
        logger.info(f"Removed {removed} duplicate records")
        
        return df_clean.reset_index(drop=True)
        
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'auto') -> pd.DataFrame:
        """
        Handle missing values using various strategies
        
        Args:
            df: Input DataFrame
            strategy: 'auto', 'drop', 'mean', 'median', 'mode', 'forward_fill'
            
        Returns:
            DataFrame with handled missing values
        """
        df_clean = df.copy()
        missing_before = df.isnull().sum().sum()
        
        if strategy == 'auto':
            # Intelligent handling based on data type and missing percentage
            for col in df.columns:
                missing_pct = df[col].isnull().sum() / len(df) * 100
                
                # Drop column if >50% missing
                if missing_pct > 50:
                    logger.warning(f"Dropping {col}: {missing_pct:.1f}% missing")
                    df_clean = df_clean.drop(columns=[col])
                    continue
                
                # Handle based on dtype
                if df[col].dtype in ['int64', 'float64']:
                    # Use median for numerical
                    df_clean[col].fillna(df[col].median(), inplace=True)
                    # Add missing indicator
                    if missing_pct > 5:
                        df_clean[f'{col}_missing'] = df[col].isnull().astype(int)
                else:
                    # Use mode for categorical
                    mode_value = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
                    df_clean[col].fillna(mode_value, inplace=True)
                    
        elif strategy == 'drop':
            df_clean = df_clean.dropna()
            
        elif strategy == 'mean':
            numerical_cols = df_clean.select_dtypes(include=[np.number]).columns
            df_clean[numerical_cols] = df_clean[numerical_cols].fillna(df_clean[numerical_cols].mean())
            
        elif strategy == 'median':
            numerical_cols = df_clean.select_dtypes(include=[np.number]).columns
            df_clean[numerical_cols] = df_clean[numerical_cols].fillna(df_clean[numerical_cols].median())
            
        elif strategy == 'mode':
            for col in df_clean.columns:
                df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
                
        missing_after = df_clean.isnull().sum().sum()
        self.cleaning_report['missing_values_handled'] = missing_before - missing_after
        logger.info(f"Handled {missing_before - missing_after} missing values")
        
        return df_clean
        
    def handle_outliers(self, df: pd.DataFrame, columns: List[str], 
                       method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
        """
        Detect and handle outliers
        
        Args:
            df: Input DataFrame
            columns: Columns to check for outliers
            method: 'iqr' or 'zscore'
            threshold: IQR multiplier or Z-score threshold
            
        Returns:
            DataFrame with handled outliers
        """
        df_clean = df.copy()
        outliers_count = 0
        
        for col in columns:
            if col not in df.columns or df[col].dtype not in ['int64', 'float64']:
                continue
                
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                # Cap outliers instead of removing
                outliers = ((df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)).sum()
                df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
                outliers_count += outliers
                
            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outliers = (z_scores > threshold).sum()
                df_clean = df_clean[z_scores <= threshold]
                outliers_count += outliers
                
        self.cleaning_report['outliers_handled'] = outliers_count
        logger.info(f"Handled {outliers_count} outliers using {method} method")
        
        return df_clean
        
    def convert_data_types(self, df: pd.DataFrame, type_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Convert column data types
        
        Args:
            df: Input DataFrame
            type_mapping: Dictionary mapping column names to desired types
            
        Returns:
            DataFrame with converted types
        """
        df_clean = df.copy()
        
        for col, dtype in type_mapping.items():
            if col in df_clean.columns:
                try:
                    if dtype == 'category':
                        df_clean[col] = df_clean[col].astype('category')
                    elif dtype == 'datetime':
                        df_clean[col] = pd.to_datetime(df_clean[col])
                    else:
                        df_clean[col] = df_clean[col].astype(dtype)
                    logger.info(f"Converted {col} to {dtype}")
                except Exception as e:
                    logger.warning(f"Could not convert {col} to {dtype}: {str(e)}")
                    
        return df_clean
        
    def standardize_text(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Standardize text columns (lowercase, strip whitespace)
        
        Args:
            df: Input DataFrame
            columns: Text columns to standardize
            
        Returns:
            DataFrame with standardized text
        """
        df_clean = df.copy()
        
        for col in columns:
            if col in df_clean.columns and df_clean[col].dtype == 'object':
                df_clean[col] = df_clean[col].str.strip().str.lower()
                logger.info(f"Standardized text in {col}")
                
        return df_clean
        
    def get_cleaning_report(self) -> Dict[str, Any]:
        """
        Get summary of cleaning operations performed
        
        Returns:
            Dictionary with cleaning statistics
        """
        return self.cleaning_report
        
    def clean_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Complete cleaning pipeline
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("Starting data cleaning pipeline...")
        
        # Step 1: Remove duplicates
        df = self.remove_duplicates(df)
        
        # Step 2: Handle missing values
        df = self.handle_missing_values(df, strategy='auto')
        
        # Step 3: Handle outliers in numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        df = self.handle_outliers(df, numerical_cols, method='iqr', threshold=1.5)
        
        # Step 4: Standardize text columns
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        df = self.standardize_text(df, text_cols)
        
        logger.info("Data cleaning pipeline completed")
        logger.info(f"Cleaning report: {self.get_cleaning_report()}")
        
        return df


if __name__ == "__main__":
    # Example usage
    # Create sample dirty data
    sample_data = {
        'customer_id': [1, 2, 3, 4, 5, 5],  # Duplicate
        'age': [25, 35, np.nan, 45, 200],  # Missing and outlier
        'income': [50000, 60000, 70000, 80000, 90000],
        'city': ['  NEW YORK  ', 'los angeles', 'CHICAGO', np.nan, 'Houston']
    }
    
    df = pd.DataFrame(sample_data)
    print("Original Data:")
    print(df)
    print()
    
    cleaner = DataCleaner()
    df_clean = cleaner.clean_pipeline(df)
    
    print("\nCleaned Data:")
    print(df_clean)
    print("\nCleaning Report:")
    print(cleaner.get_cleaning_report())
