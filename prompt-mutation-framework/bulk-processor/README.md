# Bulk CSV Processor

Asynchronous batch processing system for generating marketplace descriptions at scale using Celery + Redis.

## Features

- ✅ **CSV Upload**: Upload spreadsheet with 100+ items
- ⚙️ **Async Processing**: Celery task queue with Redis backend
- 📊 **Progress Tracking**: Real-time status updates per item
- 📥 **Download Results**: Export generated descriptions to CSV
- 🔄 **Retry Logic**: Auto-retry failed items (3 attempts)
- 🚀 **Scalable**: Process 1000+ items concurrently

## Quick Start

```bash
# 1. Start Redis + Celery worker via Docker
docker-compose up -d

# 2. Start API server
cd bulk-processor
python api.py

# 3. Upload CSV
curl -X POST http://localhost:8001/api/upload \
  -F "file=@items.csv" \
  -F "api_key=sk-ant-xxx"

# 4. Download results
curl http://localhost:8001/api/download/{job_id} -o results.csv
```

## Architecture

- **FastAPI**: REST API for CSV upload/download
- **Celery**: Distributed task queue
- **Redis**: Message broker + result backend
- **Docker**: Containerized deployment

## CSV Format

### Input CSV

| item_category | brand_model | condition | defects | price_asking | target_platform | target_language |
|---------------|-------------|-----------|---------|--------------|-----------------|-----------------|
| smartphones | iPhone 13 Pro 256GB | excellent | small scratch | 549 | eBay.de | de |
| laptops | MacBook Pro M1 16GB | good | keyboard wear | 899 | eBay.com | en |

### Output CSV

Input columns + 3 new columns:

| ... | variant_a_emotion | variant_b_value | variant_c_trust |
|-----|-------------------|-----------------|-----------------|
| ... | Sparen Sie! Apple📸★★★★ €549 | ... | ... |

## Endpoints

- `POST /api/upload` - Upload CSV, returns `{job_id}`
- `GET /api/status/{job_id}` - Check progress
- `GET /api/download/{job_id}` - Download results CSV

## Deployment

See [deployment guide](./DEPLOYMENT.md) for production setup.

**Status**: ✅ Production-Ready

**Capacity**: 1000+ items/hour (10 workers)
