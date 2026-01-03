# 🚀 How to Use the ML Engineer Project

## Quick Start (5 Minutes)

### Option 1: Run with Docker (Recommended)

```bash
# 1. Navigate to project directory
cd /Users/sunilkumar/Downloads/Python_revision/projects/ml_engineer_project

# 2. Start all services
docker-compose up -d

# 3. Check health
curl http://localhost:8000/health
# Response: {"status": "healthy"}

# 4. Make a prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST001",
    "age": 42,
    "tenure_months": 24,
    "monthly_charges": 89.99,
    "total_charges": 2159.76,
    "support_calls": 2,
    "internet_service": "Fiber",
    "contract": "One year",
    "payment_method": "Electronic check"
  }'

# 5. View API documentation
# Open browser: http://localhost:8000/docs
```

### Option 2: Run Locally (For Development)

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train model (first time only)
python -m src.models.train

# 4. Start API
uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000

# 5. Test in another terminal
curl http://localhost:8000/health
```

---

## 📖 Detailed Usage Guide

### 1. Training a New Model

#### Step 1: Prepare Your Data

**CSV Format:**
```csv
customer_id,age,gender,tenure_months,monthly_charges,total_charges,internet_service,contract,payment_method,support_calls,churn
CUST001,42,Male,24,89.99,2159.76,Fiber,One year,Electronic check,2,No
CUST002,28,Female,3,45.50,136.50,DSL,Month-to-month,Mailed check,15,Yes
```

**Required Columns:**
- `customer_id` (string)
- `age` (integer, 18-100)
- `tenure_months` (integer, >= 0)
- `monthly_charges` (float, > 0)
- `total_charges` (float, >= 0)
- `support_calls` (integer, >= 0)
- `internet_service` (string: DSL/Fiber/None)
- `contract` (string: Month-to-month/One year/Two year)
- `payment_method` (string)
- `churn` (string: Yes/No or boolean)

#### Step 2: Configure Training

Edit `config/config.yaml`:
```yaml
data:
  input_path: "data/your_data.csv"
  test_size: 0.2
  random_state: 42

model:
  type: "xgboost"
  hyperparameters:
    max_depth: 5
    learning_rate: 0.1
    n_estimators: 200
    subsample: 0.9

training:
  use_smote: true
  cross_validation_folds: 5
  hyperparameter_tuning: true

mlflow:
  tracking_uri: "http://localhost:5000"
  experiment_name: "churn_prediction"
```

#### Step 3: Run Training

```bash
# Full training pipeline
python -m src.models.train

# Expected output:
# Loading data from data/your_data.csv...
# Loaded 100,000 rows, 25 columns
# Cleaning data...
# Removed 234 duplicates
# Filled 1,245 missing values
# Engineering features...
# Created 25 features
# Training model...
# Hyperparameter tuning: 100%|███████████| 100/100 [1:23:45<00:00]
# Best parameters: {'max_depth': 5, 'learning_rate': 0.1, ...}
# Training final model...
# Evaluating model...
# Accuracy: 89.2%
# Precision: 87.3%
# Recall: 91.1%
# F1-Score: 89.2%
# Saving model to models/churn_model.pkl...
# Logging to MLflow...
# Training complete!
```

#### Step 4: Verify Model

```bash
# Check model file exists
ls -lh models/churn_model.pkl
# -rw-r--r--  1 user  staff   8.5M Dec 15 14:23 models/churn_model.pkl

# View MLflow UI
# Open browser: http://localhost:5000
# Navigate to "churn_prediction" experiment
# View metrics, parameters, and artifacts
```

### 2. Making Predictions

#### Single Prediction (via API)

**Using curl:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST12345",
    "age": 35,
    "tenure_months": 12,
    "monthly_charges": 75.50,
    "total_charges": 906.00,
    "support_calls": 3,
    "internet_service": "Fiber",
    "contract": "Month-to-month",
    "payment_method": "Electronic check"
  }'

# Response:
{
  "customer_id": "CUST12345",
  "churn_probability": 0.643,
  "will_churn": true,
  "risk_level": "high",
  "recommendation": "Urgent: Personal outreach needed. Consider retention offer.",
  "timestamp": "2024-12-15T14:30:45.123Z",
  "latency_ms": 42.5
}
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
        "customer_id": "CUST12345",
        "age": 35,
        "tenure_months": 12,
        "monthly_charges": 75.50,
        "total_charges": 906.00,
        "support_calls": 3,
        "internet_service": "Fiber",
        "contract": "Month-to-month",
        "payment_method": "Electronic check"
    }
)

result = response.json()
print(f"Churn Probability: {result['churn_probability']:.1%}")
print(f"Risk Level: {result['risk_level']}")
print(f"Recommendation: {result['recommendation']}")
```

**Using JavaScript (Node.js or Browser):**
```javascript
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    customer_id: 'CUST12345',
    age: 35,
    tenure_months: 12,
    monthly_charges: 75.50,
    total_charges: 906.00,
    support_calls: 3,
    internet_service: 'Fiber',
    contract: 'Month-to-month',
    payment_method: 'Electronic check'
  })
})
.then(res => res.json())
.then(data => {
  console.log(`Churn Probability: ${(data.churn_probability * 100).toFixed(1)}%`);
  console.log(`Risk Level: ${data.risk_level}`);
  
  if (data.will_churn) {
    alert('Customer at risk! Take action now.');
  }
});
```

#### Batch Predictions (Multiple Customers)

```bash
curl -X POST "http://localhost:8000/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "customers": [
      {
        "customer_id": "CUST001",
        "age": 42,
        "tenure_months": 24,
        "monthly_charges": 89.99,
        "total_charges": 2159.76,
        "support_calls": 2,
        "internet_service": "Fiber",
        "contract": "One year",
        "payment_method": "Electronic check"
      },
      {
        "customer_id": "CUST002",
        "age": 28,
        "tenure_months": 3,
        "monthly_charges": 45.50,
        "total_charges": 136.50,
        "support_calls": 15,
        "internet_service": "DSL",
        "contract": "Month-to-month",
        "payment_method": "Mailed check"
      }
    ]
  }'

# Response:
{
  "predictions": [
    {
      "customer_id": "CUST001",
      "churn_probability": 0.15,
      "will_churn": false,
      "risk_level": "low",
      ...
    },
    {
      "customer_id": "CUST002",
      "churn_probability": 0.78,
      "will_churn": true,
      "risk_level": "high",
      ...
    }
  ],
  "total_processed": 2,
  "high_risk_count": 1,
  "processing_time_ms": 85.2
}
```

**Python batch processing:**
```python
import pandas as pd
import requests

# Load customer data
customers = pd.read_csv('customers_to_score.csv')

# Convert to list of dicts
customer_list = customers.to_dict('records')

# Batch predict (max 1000 at a time)
batch_size = 1000
results = []

for i in range(0, len(customer_list), batch_size):
    batch = customer_list[i:i+batch_size]
    
    response = requests.post(
        "http://localhost:8000/predict/batch",
        json={"customers": batch}
    )
    
    batch_results = response.json()['predictions']
    results.extend(batch_results)

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv('churn_predictions.csv', index=False)

print(f"Processed {len(results)} customers")
print(f"High risk: {len(results_df[results_df['risk_level'] == 'high'])}")
```

### 3. Monitoring the System

#### View Metrics Dashboard

```bash
# Start Grafana (if using Docker Compose)
# Open browser: http://localhost:3000
# Login: admin / admin

# Pre-configured dashboards:
# 1. API Performance
# 2. Model Performance
# 3. Infrastructure Health
```

#### Check Prometheus Metrics

```bash
# View raw metrics
curl http://localhost:8000/metrics

# Example output:
# churn_predictions_total{risk_level="high"} 1234
# churn_predictions_total{risk_level="medium"} 5678
# churn_predictions_total{risk_level="low"} 12345
# churn_prediction_latency_seconds_bucket{le="0.05"} 15234
# churn_model_accuracy 0.892
```

#### Monitor Data Drift

```bash
# Run drift detection
python -m src.monitoring.metrics --check-drift

# Output:
# Checking data drift...
# Feature: tenure_months, PSI: 0.08 ✅ No drift
# Feature: monthly_charges, PSI: 0.15 ⚠️ Monitor closely
# Feature: support_calls, PSI: 0.28 🚨 DRIFT DETECTED!
# 
# Recommendation: Retrain model with recent data
```

### 4. Retraining the Model

#### Automated Retraining

```python
# Check if retraining is needed
python -m src.monitoring.metrics --should-retrain

# Output:
# Checking retraining criteria...
# ✅ Data drift: PSI = 0.28 (threshold: 0.25)
# ✅ Performance degradation: Accuracy = 85% (baseline: 89%)
# ❌ Time since training: 15 days (threshold: 30 days)
# 
# Result: RETRAINING RECOMMENDED
# Reasons: Data drift detected, Performance degradation

# Trigger retraining
python -m src.models.retrain

# This will:
# 1. Extract last 6 months of production data
# 2. Include ground truth labels
# 3. Run full pipeline (clean, engineer, train)
# 4. Evaluate new model
# 5. A/B test against current model
# 6. Deploy if better
```

#### Manual Retraining

```bash
# Retrain with new data
python -m src.models.train \
  --data-path data/new_data.csv \
  --model-name churn_model_v2 \
  --experiment-name churn_prediction_v2

# Compare models in MLflow
# Open: http://localhost:5000
# Compare runs side-by-side

# Deploy new model manually
cp models/churn_model_v2.pkl models/churn_model.pkl

# Restart API to load new model
docker-compose restart api
```

### 5. Testing

#### Run Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Open coverage report
open htmlcov/index.html
```

#### Run Integration Tests

```bash
# Test full pipeline
pytest tests/test_pipeline.py -v

# Test API endpoints
pytest tests/test_api.py -v
```

#### Manual API Testing

**Interactive API docs (Swagger UI):**
```
1. Open browser: http://localhost:8000/docs
2. Click on endpoint (e.g., POST /predict)
3. Click "Try it out"
4. Fill in example data
5. Click "Execute"
6. See response
```

### 6. Adding Your Own Data

#### Prepare Data

```python
import pandas as pd

# Your raw data
data = pd.read_csv('your_raw_data.csv')

# Required transformations
data['customer_id'] = data['id'].astype(str)
data['age'] = data['customer_age'].astype(int)
data['tenure_months'] = data['tenure_days'] / 30
data['churn'] = data['is_churned'].map({1: 'Yes', 0: 'No'})

# Save in required format
data.to_csv('data/prepared_data.csv', index=False)
```

#### Update Configuration

```yaml
# config/config.yaml
data:
  input_path: "data/prepared_data.csv"
  required_columns:
    - customer_id
    - age
    - tenure_months
    - monthly_charges
    - total_charges
    - support_calls
    - internet_service
    - contract
    - payment_method
    - churn
```

#### Validate Data

```python
# Validate before training
python -m src.data_pipeline.data_loader \
  --validate data/prepared_data.csv

# Output:
# ✅ All required columns present
# ✅ No missing values in key columns
# ✅ Data types correct
# ⚠️ Warning: 5% missing values in 'support_calls' (will be imputed)
# ✅ Data ready for training
```

### 7. Customization

#### Change Model Parameters

```yaml
# config/config.yaml
model:
  hyperparameters:
    max_depth: 7  # Increase for more complex patterns
    learning_rate: 0.05  # Decrease for more stable training
    n_estimators: 300  # Increase for better performance
    subsample: 0.8  # Decrease to prevent overfitting
```

#### Add Custom Features

```python
# src/data_pipeline/feature_engineer.py

class FeatureEngineer:
    def create_custom_features(self, df):
        """Add your own domain-specific features"""
        
        # Example: Customer engagement score
        df['engagement_score'] = (
            df['data_usage_gb'] * 0.3 +
            df['call_minutes'] * 0.2 +
            df['sms_count'] * 0.1 +
            df['service_count'] * 0.4
        )
        
        # Example: Payment reliability
        df['payment_reliability'] = (
            1 - (df['late_payments'] / (df['tenure_months'] + 1))
        )
        
        # Example: Price sensitivity
        df['price_sensitivity'] = (
            df['monthly_charges'] / df['income']
        )
        
        return df
```

#### Modify Risk Thresholds

```python
# src/api/app.py

@app.post("/predict")
def predict_churn(customer: CustomerData):
    # ... existing code ...
    
    # Custom risk levels
    if probability < 0.2:
        risk = "very_low"
        recommendation = "No action needed"
    elif probability < 0.4:
        risk = "low"
        recommendation = "Monitor engagement"
    elif probability < 0.6:
        risk = "medium"
        recommendation = "Send retention email"
    elif probability < 0.8:
        risk = "high"
        recommendation = "Call customer service"
    else:
        risk = "critical"
        recommendation = "Urgent: Executive intervention"
    
    # ... rest of code ...
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "Model file not found"

```bash
# Error: FileNotFoundError: models/churn_model.pkl

# Solution: Train the model first
python -m src.models.train
```

#### 2. "Database connection failed"

```bash
# Error: Could not connect to PostgreSQL

# Check if database is running
docker-compose ps

# Restart database
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

#### 3. "Redis connection timeout"

```bash
# Error: redis.exceptions.TimeoutError

# Check Redis
docker-compose ps redis

# Restart Redis
docker-compose restart redis

# Or disable caching temporarily
# In src/api/app.py, set USE_CACHE = False
```

#### 4. "API returns 500 error"

```bash
# Check API logs
docker-compose logs api

# Or if running locally
# Check terminal output

# Common causes:
# - Missing model file
# - Invalid input data
# - Database connection issues
```

#### 5. "Predictions are all the same"

```bash
# Possible causes:
# 1. Model not trained properly
# 2. Features not scaled correctly
# 3. Data drift

# Check model evaluation metrics
python -m src.models.train --evaluate-only

# If accuracy is low, retrain:
python -m src.models.train
```

### Performance Issues

#### Slow Predictions

```bash
# Check latency
curl http://localhost:8000/metrics | grep latency

# If > 100ms:
# 1. Enable Redis caching
# 2. Increase API replicas
# 3. Optimize feature engineering

# Profile code
python -m cProfile -s cumtime src/api/app.py
```

#### High Memory Usage

```bash
# Check memory
docker stats

# If > 2GB:
# 1. Reduce batch size
# 2. Clear cache periodically
# 3. Use model quantization

# Restart with memory limit
docker-compose up -d --scale api=3 \
  --memory="1g" --memory-swap="2g"
```

---

## 📚 Additional Resources

### API Documentation
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

### Monitoring Dashboards
- MLflow: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

### Logs
```bash
# API logs
docker-compose logs api -f

# Database logs
docker-compose logs postgres -f

# All logs
docker-compose logs -f
```

### Configuration Files
- Model config: `config/config.yaml`
- Docker setup: `docker-compose.yml`
- Dependencies: `requirements.txt`

---

## 🎯 Best Practices

1. **Always retrain when**:
   - Data drift PSI > 0.25
   - Accuracy drops > 5%
   - 30 days since last training

2. **Monitor these metrics**:
   - Prediction latency (< 100ms)
   - Error rate (< 1%)
   - Model accuracy (> 85%)
   - Cache hit rate (> 30%)

3. **Security**:
   - Use API keys in production
   - Enable HTTPS/TLS
   - Don't log sensitive data
   - Rotate credentials regularly

4. **Scaling**:
   - Start with 1 API container
   - Scale horizontally (not vertically)
   - Use load balancer
   - Enable auto-scaling

5. **Testing**:
   - Run tests before deployment
   - A/B test new models
   - Monitor for 24h after deployment
   - Keep rollback ready

---

## ✅ Quick Reference

| Task | Command |
|------|---------|
| Start system | `docker-compose up -d` |
| Stop system | `docker-compose down` |
| Train model | `python -m src.models.train` |
| Make prediction | `curl -X POST http://localhost:8000/predict -d '{...}'` |
| View API docs | Browser: `http://localhost:8000/docs` |
| Check health | `curl http://localhost:8000/health` |
| Run tests | `pytest tests/ -v` |
| View logs | `docker-compose logs api -f` |
| Restart API | `docker-compose restart api` |
| Scale API | `docker-compose up -d --scale api=3` |

---

**Need more help?** See [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md) for detailed explanations or [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) for technical details.
