# Lab8: Titanic Survival Predictor - MLOps Pipeline

A complete ML deployment pipeline with FastAPI, Docker, Prometheus monitoring, and Grafana dashboards.

## Project Structure
```
Lab8/
├── data/                        # Titanic dataset
├── src/
│   ├── app.py                   # FastAPI REST API with metrics
│   ├── train.py                 # Model training script
│   ├── model_utils.py           # Preprocessing pipeline
│   ├── logger_config.py         # Structured logging
│   ├── requirements.txt         # Python dependencies
│   └── tests/
│       └── test_app.py         # API tests
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Multi-service orchestration
├── prometheus.yml               # Metrics scraping config
├── grafana/                     # Dashboard provisioning
└── .github/workflows/ci-cd.yml  # CI/CD pipeline
```

## Features
- **ML Model**: RandomForest classifier trained on Titanic dataset (79% accuracy)
- **REST API**: FastAPI with `/predict` endpoint and `/metrics` for monitoring
- **Monitoring**: Prometheus metrics collection (request counts, latency, predictions)
- **Logging**: Structured JSON logs with structlog
- **Containerization**: Docker with multi-stage build and model training
- **Orchestration**: Docker Compose for app, Prometheus, and Grafana
- **CI/CD**: GitHub Actions workflow for testing and deployment

## Quick Start

### 1. Run Locally (with virtual environment)
```bash
# Download dataset
curl -o data/train.csv https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv

# Install dependencies
pip install -r src/requirements.txt

# Train model
cd src && python train.py

# Start API server
uvicorn app:app --reload

# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"Age": 30, "Fare": 7.25, "Sex": "male", "Embarked": "S", "Pclass": "3"}}'
```

### 2. Run with Docker Compose (Recommended)
```bash
# Build and start all services
docker compose up --build -d

# Check container status
docker compose ps

# View logs
docker logs ds_app

# Test the API
curl http://localhost:8000/
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"Age": 28, "Fare": 50, "Sex": "female", "Embarked": "C", "Pclass": "1"}}'

# Stop all services
docker compose down
```

## Access Points
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Metrics**: http://localhost:8000/metrics
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## API Usage

### Root Endpoint
```bash
curl http://localhost:8000/
# Response: {"message": "Titanic Survival Predictor API"}
```

### Prediction Endpoint
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "Age": 30,
      "Fare": 7.25,
      "Sex": "male",
      "Embarked": "S",
      "Pclass": "3"
    }
  }'
# Response: {"prediction": 0, "probability": 0.98}
# 0 = Did not survive, 1 = Survived
```

### Metrics Endpoint
```bash
curl http://localhost:8000/metrics
# Returns Prometheus-formatted metrics
```

## Monitoring

### Prometheus Metrics
- `api_requests_total`: Counter for all API requests by endpoint, method, and status
- `prediction_latency_seconds`: Histogram of prediction latency
- `prediction_class_total`: Counter for predictions by class (0 or 1)

### Grafana Dashboard
1. Open http://localhost:3000
2. Login with admin/admin
3. Add Prometheus data source: http://prometheus:9090
4. Create dashboards to visualize:
   - Request rate and error rate
   - Prediction latency (p50, p95, p99)
   - Prediction distribution (survived vs not survived)

## Model Information
- **Algorithm**: RandomForest Classifier (100 estimators)
- **Features**: Age, Fare, Sex, Embarked, Pclass
- **Preprocessing**: Median imputation for Age/Fare, mode imputation for categorical features, StandardScaler, OneHotEncoder
- **Performance**: ~79% accuracy on test set

## Testing
```bash
# Run tests
pytest -v

# Run specific test
pytest src/tests/test_app.py::test_predict_minimal -v
```

## CI/CD
The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) automatically:
1. Runs tests on push/PR to main
2. Builds Docker image on main branch
3. Optionally pushes to Docker Hub (requires secrets)

## Development

### Retrain Model
```bash
cd src
python train.py
# Model saved to src/model.joblib
```

### Update Dependencies
```bash
# Update src/requirements.txt
pip install -r src/requirements.txt
```

### Rebuild Docker Image
```bash
docker compose up --build -d app
```

## Troubleshooting

### Model not found
Ensure `model.joblib` exists in `src/` directory. Run training script first.

### Port conflicts
Change ports in `docker-compose.yml` if 8000, 9090, or 3000 are already in use.

### Container logs
```bash
docker logs ds_app          # App logs
docker logs prometheus      # Prometheus logs
docker logs grafana         # Grafana logs
```

## Results from Lab Run
✅ Dataset downloaded (891 samples)
✅ Model trained (79.3% accuracy)
✅ Docker stack deployed successfully
✅ API working (predictions returning correctly)
✅ Prometheus scraping metrics (health: up)
✅ Structured JSON logging active
✅ All containers running

**Sample Predictions:**
- Male, 3rd class, Age 30, Fare $7.25 → **Did not survive** (98% confidence)
- Female, 1st class, Age 28, Fare $50 → **Survived** (100% confidence)

## License
Educational project for ADS Lab 8.
