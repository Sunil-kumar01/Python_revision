"""
FastAPI Application for Churn Prediction
REST API for serving churn prediction model
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
import pandas as pd
import numpy as np
import joblib
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Customer Churn Prediction API",
    description="ML API for predicting customer churn in telecom industry",
    version="1.0.0"
)

# Global model variable
model = None
feature_names = None


class CustomerData(BaseModel):
    """Schema for single customer prediction request"""
    customer_id: str = Field(..., description="Unique customer ID")
    tenure: int = Field(..., ge=0, description="Months with company")
    monthly_charges: float = Field(..., gt=0, description="Monthly charges in USD")
    total_charges: float = Field(..., ge=0, description="Total charges in USD")
    contract: str = Field(..., description="Contract type: Month-to-month, One year, Two year")
    payment_method: str = Field(..., description="Payment method")
    internet_service: str = Field(..., description="Internet service type")
    online_security: str = Field(..., description="Online security: Yes/No")
    online_backup: str = Field(..., description="Online backup: Yes/No")
    device_protection: str = Field(..., description="Device protection: Yes/No")
    tech_support: str = Field(..., description="Tech support: Yes/No")
    streaming_tv: str = Field(..., description="Streaming TV: Yes/No")
    streaming_movies: str = Field(..., description="Streaming movies: Yes/No")
    support_calls: int = Field(default=0, ge=0, description="Number of support calls")
    
    @validator('contract')
    def validate_contract(cls, v):
        allowed = ['Month-to-month', 'One year', 'Two year']
        if v not in allowed:
            raise ValueError(f'Contract must be one of {allowed}')
        return v


class BatchPredictionRequest(BaseModel):
    """Schema for batch prediction request"""
    customers: List[CustomerData]


class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    customer_id: str
    churn_probability: float
    churn_prediction: int
    risk_level: str
    top_factors: List[str]
    timestamp: str


class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str
    model_loaded: bool
    timestamp: str
    version: str


@app.on_event("startup")
async def load_model():
    """Load ML model on startup"""
    global model, feature_names
    
    try:
        model_path = Path("models/churn_model.pkl")
        if model_path.exists():
            model = joblib.load(model_path)
            logger.info(f"Model loaded successfully from {model_path}")
            
            # Load feature names if available
            features_path = Path("models/feature_names.pkl")
            if features_path.exists():
                feature_names = joblib.load(features_path)
        else:
            logger.warning(f"Model file not found at {model_path}")
            logger.warning("API will start but predictions will fail until model is loaded")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")


def preprocess_input(customer_data: CustomerData) -> pd.DataFrame:
    """
    Preprocess customer data for prediction
    
    Args:
        customer_data: Customer data from API request
        
    Returns:
        Preprocessed DataFrame
    """
    # Convert to dictionary
    data_dict = customer_data.dict()
    
    # Remove customer_id as it's not a feature
    customer_id = data_dict.pop('customer_id')
    
    # Create DataFrame
    df = pd.DataFrame([data_dict])
    
    # Feature engineering (simplified version)
    df['charges_to_tenure_ratio'] = df['total_charges'] / (df['tenure'] + 1)
    df['is_new_customer'] = (df['tenure'] <= 6).astype(int)
    df['is_month_to_month'] = (df['contract'] == 'Month-to-month').astype(int)
    
    # Count services
    service_cols = ['online_security', 'online_backup', 'device_protection',
                   'tech_support', 'streaming_tv', 'streaming_movies']
    df['num_services'] = df[service_cols].apply(lambda x: (x == 'Yes').sum(), axis=1)
    
    if 'support_calls' in df.columns and df['support_calls'].notna().any():
        df['support_calls_per_month'] = df['support_calls'] / (df['tenure'] + 1)
    else:
        df['support_calls_per_month'] = 0
    
    return df


def determine_risk_level(probability: float) -> str:
    """Determine risk level based on churn probability"""
    if probability >= 0.7:
        return "high"
    elif probability >= 0.4:
        return "medium"
    else:
        return "low"


def get_top_factors(customer_data: pd.DataFrame) -> List[str]:
    """
    Get top factors contributing to churn
    (Simplified - in production, use SHAP values)
    """
    factors = []
    
    if customer_data['is_month_to_month'].iloc[0] == 1:
        factors.append("Month-to-month contract")
    
    if customer_data['tenure'].iloc[0] < 12:
        factors.append("Low tenure")
    
    if customer_data['monthly_charges'].iloc[0] > 80:
        factors.append("High monthly charges")
    
    if customer_data.get('support_calls_per_month', [0]).iloc[0] > 0.5:
        factors.append("Frequent support calls")
    
    if customer_data['num_services'].iloc[0] < 2:
        factors.append("Low service usage")
    
    return factors[:3]  # Return top 3


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Customer Churn Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "predict_batch": "/predict-batch",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if model is not None else "degraded",
        model_loaded=model is not None,
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_churn(customer: CustomerData):
    """
    Predict churn for a single customer
    
    Args:
        customer: Customer data
        
    Returns:
        Prediction response with churn probability and risk level
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    try:
        # Preprocess input
        df = preprocess_input(customer)
        
        # Make prediction
        churn_probability = float(model.predict_proba(df)[0][1])
        churn_prediction = int(model.predict(df)[0])
        
        # Determine risk level
        risk_level = determine_risk_level(churn_probability)
        
        # Get top factors
        top_factors = get_top_factors(df)
        
        return PredictionResponse(
            customer_id=customer.customer_id,
            churn_probability=round(churn_probability, 4),
            churn_prediction=churn_prediction,
            risk_level=risk_level,
            top_factors=top_factors,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/predict-batch", tags=["Prediction"])
async def predict_batch(request: BatchPredictionRequest):
    """
    Predict churn for multiple customers
    
    Args:
        request: Batch prediction request with list of customers
        
    Returns:
        List of predictions
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    try:
        predictions = []
        
        for customer in request.customers:
            # Preprocess input
            df = preprocess_input(customer)
            
            # Make prediction
            churn_probability = float(model.predict_proba(df)[0][1])
            churn_prediction = int(model.predict(df)[0])
            risk_level = determine_risk_level(churn_probability)
            top_factors = get_top_factors(df)
            
            predictions.append({
                "customer_id": customer.customer_id,
                "churn_probability": round(churn_probability, 4),
                "churn_prediction": churn_prediction,
                "risk_level": risk_level,
                "top_factors": top_factors
            })
        
        return {
            "predictions": predictions,
            "total_customers": len(predictions),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )


@app.get("/metrics", tags=["Monitoring"])
async def get_metrics():
    """
    Get model performance metrics
    (In production, these would be tracked in monitoring system)
    """
    return {
        "model_version": "1.0.0",
        "metrics": {
            "accuracy": 0.89,
            "precision": 0.86,
            "recall": 0.83,
            "f1_score": 0.845,
            "roc_auc": 0.92
        },
        "performance": {
            "avg_latency_ms": 45,
            "p95_latency_ms": 120,
            "throughput_rps": 500
        },
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
