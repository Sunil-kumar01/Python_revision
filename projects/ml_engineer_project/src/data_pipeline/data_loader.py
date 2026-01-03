"""
Data Loader Module
Handles loading data from various sources (CSV, Database, S3)
"""

import pandas as pd
import logging
from typing import Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """
    Loads customer data from various sources
    """
    
    def __init__(self, config: dict):
        """
        Initialize DataLoader
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
    def load_from_csv(self, file_path: str) -> pd.DataFrame:
        """
        Load data from CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            DataFrame with loaded data
        """
        try:
            logger.info(f"Loading data from {file_path}")
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns")
            return df
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading CSV: {str(e)}")
            raise
            
    def load_from_database(self, query: str, connection_string: str) -> pd.DataFrame:
        """
        Load data from PostgreSQL database
        
        Args:
            query: SQL query to execute
            connection_string: Database connection string
            
        Returns:
            DataFrame with query results
        """
        try:
            import psycopg2
            from sqlalchemy import create_engine
            
            logger.info("Connecting to database...")
            engine = create_engine(connection_string)
            df = pd.read_sql(query, engine)
            logger.info(f"Loaded {len(df)} records from database")
            return df
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            raise
            
    def load_from_s3(self, bucket: str, key: str) -> pd.DataFrame:
        """
        Load data from AWS S3
        
        Args:
            bucket: S3 bucket name
            key: S3 object key
            
        Returns:
            DataFrame with S3 data
        """
        try:
            import boto3
            from io import StringIO
            
            logger.info(f"Loading data from S3: {bucket}/{key}")
            s3_client = boto3.client('s3')
            obj = s3_client.get_object(Bucket=bucket, Key=key)
            df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
            logger.info(f"Loaded {len(df)} records from S3")
            return df
        except Exception as e:
            logger.error(f"S3 error: {str(e)}")
            raise
            
    def validate_schema(self, df: pd.DataFrame, required_columns: list) -> bool:
        """
        Validate that DataFrame has required columns
        
        Args:
            df: DataFrame to validate
            required_columns: List of required column names
            
        Returns:
            True if valid, raises exception otherwise
        """
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        logger.info("Schema validation passed")
        return True
        
    def get_data_summary(self, df: pd.DataFrame) -> dict:
        """
        Get summary statistics of the dataset
        
        Args:
            df: DataFrame to summarize
            
        Returns:
            Dictionary with summary statistics
        """
        summary = {
            'total_records': len(df),
            'total_features': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
            'missing_values': df.isnull().sum().to_dict(),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'duplicates': df.duplicated().sum()
        }
        
        logger.info(f"Dataset summary: {summary['total_records']} records, "
                   f"{summary['total_features']} features, "
                   f"{summary['duplicates']} duplicates")
        
        return summary


if __name__ == "__main__":
    # Example usage
    config = {'data': {'raw_data_path': 'data/raw/customer_data.csv'}}
    loader = DataLoader(config)
    
    # Create sample data if file doesn't exist
    sample_data_path = "data/raw/customer_data.csv"
    if not os.path.exists(sample_data_path):
        print(f"Sample data not found. You would load real data here.")
    else:
        df = loader.load_from_csv(sample_data_path)
        summary = loader.get_data_summary(df)
        print(summary)
