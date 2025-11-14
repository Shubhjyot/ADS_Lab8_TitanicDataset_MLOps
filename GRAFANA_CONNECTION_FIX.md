# 🔧 QUICK FIX: Grafana Connection Error

## ❌ The Problem
You saw this error:
```
Post "http://localhost:9090/api/v1/query": dial tcp [::1]:9090: 
connect: connection refused - There was an error returned 
querying the Prometheus API.
```

## ✅ The Solution

### Use the correct URL in Grafana:

```
http://prometheus:9090
```

**NOT:**
- ~~http://localhost:9090~~ ❌
- ~~prometheus:9090~~ ❌ (missing http://)
- ~~http://prometheus~~ ❌ (missing :9090)

---

## 📝 Step-by-Step Fix

1. **Open Grafana**: http://localhost:3000
2. **Login**: admin / admin
3. **Navigate**: ☰ menu → **Connections** → **Data sources**
4. **Edit or Add**: 
   - If Prometheus exists, click on it
   - If not, click **"Add data source"** → **"Prometheus"**
5. **Set URL**: `http://prometheus:9090`
6. **Click**: Scroll down → **"Save & Test"**
7. **Success**: You should see ✅ green checkmark with "Data source is working"

---

## 🎯 Quick Copy-Paste

**Data Source Configuration:**
```yaml
Name: Prometheus
Type: Prometheus
URL: http://prometheus:9090
Access: Server (default)
```

---

## 💡 Why This Works

Docker Compose creates an internal network. Containers talk to each other using **service names**:

| From Where | URL to Use |
|------------|------------|
| Your Browser → Prometheus | `http://localhost:9090` |
| Your Browser → Grafana | `http://localhost:3000` |
| Grafana → Prometheus | `http://prometheus:9090` |
| Prometheus → App | `http://app:8000` |

---

## 🧪 Test It's Working

After configuring the data source:

1. In Grafana, click **"Explore"** (compass icon in sidebar)
2. Select **"Prometheus"** from dropdown
3. Enter query: `up`
4. Click **"Run query"**
5. You should see: **Value = 1** ✅

---

## 📊 Next: Create a Dashboard

After data source is connected:

1. ☰ menu → **Dashboards** → **"New"** → **"Import"**
2. **Upload file**: `grafana/titanic-dashboard.json`
3. **Click Import**
4. 🎉 Dashboard appears with 4 panels!

Or try these queries manually:
- `api_requests_total` - Total API requests
- `prediction_class_total` - Predictions by class
- `rate(api_requests_total[1m])` - Request rate per second

---

## 🆘 Still Not Working?

**Check containers are running:**
```bash
docker compose ps
```

**Check Prometheus is accessible:**
```bash
curl http://localhost:9090/-/healthy
```

**Check from inside Grafana container:**
```bash
docker exec grafana curl http://prometheus:9090/api/v1/query?query=up
```

**View logs:**
```bash
docker logs grafana
docker logs prometheus
```

---

## ✅ Expected Result

After fixing, when you click "Save & Test":

```
✅ Data source is working
✅ Successfully queried the Prometheus API
```

Then you can create dashboards and visualize your ML metrics! 📈
