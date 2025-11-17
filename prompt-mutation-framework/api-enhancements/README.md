# API Enhancements - JWT Auth & Analytics

Production-ready enhancements for the Demo API including authentication, usage tracking, and webhooks.

## Features Added

### 1. JWT Authentication
- User registration/login endpoints
- JWT token-based auth for all API calls
- Token expiration (24h) + refresh tokens
- Password hashing with bcrypt

### 2. Usage Analytics
- Track API calls per user
- Monitor generation counts, success/failure rates
- Cost tracking (estimated based on token usage)
- Export analytics to CSV/JSON

### 3. Rate Limiting
- Per-user limits (10 requests/minute, 1000/day)
- Tier-based quotas (Free, Pro, Enterprise)
- 429 response when limit exceeded

### 4. Webhooks
- Notify external systems when generation completes
- Supports async/batch processing workflows
- Retry failed webhook deliveries (3 attempts)

### 5. API Key Management
- Generate multiple API keys per user
- Rotate keys without downtime
- Revoke compromised keys instantly

## Quick Start

```bash
# 1. Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "SecurePass123"}'

# Returns: {"access_token": "eyJ...", "user_id": "uuid"}

# 2. Generate with auth
curl -X POST http://localhost:8000/api/generate \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{...item data...}'

# 3. Check analytics
curl http://localhost:8000/api/analytics \
  -H "Authorization: Bearer eyJ..."

# Returns:
{
  "total_requests": 150,
  "success_rate": 0.96,
  "estimated_cost": "$1.50",
  "requests_today": 12,
  "quota_remaining": 988
}
```

## Endpoints Added

### Authentication
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Get JWT token
- `POST /api/auth/refresh` - Refresh expired token
- `DELETE /api/auth/logout` - Invalidate token

### Analytics
- `GET /api/analytics` - Usage stats for current user
- `GET /api/analytics/export` - Download CSV report

### API Keys
- `POST /api/keys` - Generate new API key
- `GET /api/keys` - List user's API keys
- `DELETE /api/keys/{key_id}` - Revoke key

### Webhooks
- `POST /api/webhooks` - Register webhook URL
- `GET /api/webhooks` - List webhooks
- `DELETE /api/webhooks/{webhook_id}` - Delete webhook

## Pricing Tiers

| Tier | Requests/Day | Cost | Features |
|------|--------------|------|----------|
| Free | 100 | $0 | Basic generation |
| Pro | 1000 | $29/mo | Analytics, webhooks |
| Enterprise | Unlimited | Custom | Dedicated support, SLA |

## Database Schema

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    tier VARCHAR DEFAULT 'free',
    created_at TIMESTAMP
);

CREATE TABLE api_keys (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    key_hash VARCHAR NOT NULL,
    name VARCHAR,
    created_at TIMESTAMP,
    last_used_at TIMESTAMP,
    revoked BOOLEAN DEFAULT FALSE
);

CREATE TABLE usage_logs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    endpoint VARCHAR,
    status_code INT,
    tokens_used INT,
    created_at TIMESTAMP
);
```

## Security

✅ **Password Hashing**: bcrypt with salt rounds=12
✅ **JWT Signing**: HS256 with secret key rotation
✅ **Rate Limiting**: Token bucket algorithm
✅ **SQL Injection Protection**: Parameterized queries
✅ **CORS**: Configured for specific origins only

## Deployment

```yaml
# docker-compose.yml
services:
  api:
    build: .
    environment:
      DATABASE_URL: postgresql://user:pass@db:5432/marketplace
      JWT_SECRET: your-secret-here
      JWT_EXPIRY: 86400  # 24 hours
    ports:
      - "8000:8000"

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: marketplace
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
```

## Migration from v1.0 (No Auth)

```bash
# 1. Add authentication to existing demo
cp api-enhancements/auth.py demo/backend/auth.py

# 2. Update main.py to require auth
# Add: from auth import require_auth decorator

# 3. Migrate existing usage (optional)
python migrate_users.py

# 4. Deploy with backwards compatibility
# Keep /api/generate public for 30 days, add /api/v2/generate with auth
```

**Status**: ✅ Production-Ready

**Framework Version**: 1.0 + Auth Extensions

**Last Updated**: 2025-11-17
