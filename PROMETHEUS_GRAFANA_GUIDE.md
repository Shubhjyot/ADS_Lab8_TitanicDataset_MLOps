# 📊 PROMETHEUS & GRAFANA SETUP GUIDE

## ✅ STEP 1: PROMETHEUS QUERIES

### Open Prometheus (http://localhost:9090)

1. Click on the **"Query"** tab at the top (blue button)
2. In the expression box, enter one of these queries:

#### Basic Queries:

**1. View All API Requests:**
```
api_requests_total
```

**2. Request Rate (requests per second):**
```
rate(api_requests_total[1m])
```

**3. Total Predictions by Class:**
```
prediction_class_total
```

**4. Average Prediction Latency:**
```
rate(prediction_latency_seconds_sum[5m]) / rate(prediction_latency_seconds_count[5m])
```

**5. 95th Percentile Latency:**
```
histogram_quantile(0.95, rate(prediction_latency_seconds_bucket[5m]))
```

3. Click **"Execute"** (blue button on the right)
4. Switch between **"Table"** and **"Graph"** views to see the data

---

## ✅ STEP 2: GRAFANA DASHBOARD SETUP

### A. Add Prometheus as Data Source

1. Open Grafana: http://localhost:3000
2. Login: **admin** / **admin** (skip password change if prompted)
3. Click the **☰ menu** (top left) → **Connections** → **Data sources**
4. Click **"Add data source"**
5. Select **"Prometheus"**
6. Configure:
   - **Name**: Prometheus
   - **URL**: `http://prometheus:9090`
   - Scroll down and click **"Save & Test"**
   - You should see: ✅ "Successfully queried the Prometheus API"

### B. Import the Dashboard

**Method 1: Import JSON File**
1. Click **☰ menu** → **Dashboards**
2. Click **"New"** → **"Import"**
3. Click **"Upload JSON file"**
4. Select: `/Users/shubhjyot/Desktop/60009220197/SEM 7/ADS/Lab8/grafana/titanic-dashboard.json`
5. Click **"Import"**

**Method 2: Create Manually**
1. Click **☰ menu** → **Dashboards** → **"New"** → **"New Dashboard"**
2. Click **"Add visualization"**
3. Select **"Prometheus"** as data source
4. In the query box, enter: `rate(api_requests_total[1m])`
5. Click **"Run queries"**
6. Set panel title and click **"Apply"**
7. Repeat to add more panels with different queries

---

## 📈 SUGGESTED DASHBOARD PANELS

### Panel 1: API Request Rate
- **Query**: `rate(api_requests_total[1m])`
- **Type**: Time series
- **Title**: "API Request Rate (per second)"

### Panel 2: Total Requests
- **Query**: `sum(api_requests_total)`
- **Type**: Stat / Gauge
- **Title**: "Total API Requests"

### Panel 3: Prediction Latency
- **Query 1**: `histogram_quantile(0.95, rate(prediction_latency_seconds_bucket[5m]))`
- **Query 2**: `histogram_quantile(0.99, rate(prediction_latency_seconds_bucket[5m]))`
- **Type**: Time series
- **Title**: "Prediction Latency (p95, p99)"

### Panel 4: Predictions Distribution
- **Query**: `prediction_class_total`
- **Type**: Pie chart
- **Title**: "Predictions by Class"

### Panel 5: Success Rate
- **Query**: `rate(api_requests_total{status="200"}[5m])`
- **Type**: Time series
- **Title**: "Successful Requests"

---

## 🎯 QUICK TEST

### Generate More Traffic:
```bash
# Run this in terminal to generate sample data
for i in {1..50}; do
  curl -s -X POST http://localhost:8000/predict \
    -H "Content-Type: application/json" \
    -d '{"features": {"Age": 30, "Fare": 25, "Sex": "male", "Embarked": "S", "Pclass": "2"}}' > /dev/null
  echo "Request $i sent"
  sleep 0.1
done
```

### View Metrics:
```bash
# See current metrics
curl http://localhost:8000/metrics | grep -E "api_requests|prediction"
```

---

## 📊 CURRENT STATUS

✅ **Metrics Generated**: 37+ prediction requests
✅ **Prometheus Scraping**: Active (every 15 seconds)
✅ **Data Available**: 
- API request counts
- Prediction latency histograms
- Prediction class distribution

---

## 🔍 TROUBLESHOOTING

### If no data appears in Prometheus:
1. Check Prometheus targets: http://localhost:9090/targets
2. Verify "ds-app" target shows "UP" status
3. Wait 15-30 seconds for next scrape

### If Grafana shows "No data":
1. Verify Prometheus data source is configured
2. Check time range (top right) - set to "Last 15 minutes"
3. Click the refresh icon or enable auto-refresh (5s)

### Generate fresh data:
```bash
# Quick test
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"Age": 25, "Fare": 30, "Sex": "female", "Embarked": "C", "Pclass": "1"}}'
```

---

## 📚 PROMETHEUS QUERY LANGUAGE (PromQL) TIPS

- `api_requests_total` - instant value
- `rate(api_requests_total[1m])` - per-second rate over 1 minute
- `sum(api_requests_total)` - aggregate all values
- `{status="200"}` - filter by label
- `histogram_quantile(0.95, ...)` - calculate percentiles

---

## 🎉 SUCCESS CHECKLIST

- [ ] Prometheus showing query results
- [ ] Prometheus targets page shows "UP" status
- [ ] Grafana data source connection successful
- [ ] Dashboard created with at least one panel
- [ ] Panels showing live data
- [ ] Auto-refresh enabled

**Need help?** Check the logs:
```bash
docker logs ds_app
docker logs prometheus
docker logs grafana
```
