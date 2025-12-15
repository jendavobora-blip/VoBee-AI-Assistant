# Marketing Intelligence Service

Advanced PR and marketing intelligence with dynamic product promotion and analytics.

## Features

- **Product Catalog Management** - Create and manage products
- **Dynamic Promotions** - Create targeted, personalized campaigns
- **Product Bundling** - L20 tier bundles for enterprise customers
- **Marketing Analytics** - Real-time performance metrics and ROI
- **Dashboard Management** - Configuration with rollback and approval workflow
- **Mass Customization** - Scalable promotion systems

## API Endpoints

### Product Management

#### Create Product
```bash
POST /products
Content-Type: application/json

{
  "name": "AI Assistant Pro",
  "description": "Enterprise AI assistant",
  "price": 99.99,
  "category": "software",
  "tags": ["ai", "enterprise", "productivity"]
}
```

#### List Products
```bash
GET /products
```

### Promotions

#### Create Promotion
```bash
POST /promotions
Content-Type: application/json

{
  "name": "Summer Sale 2024",
  "description": "30% off all products",
  "product_ids": ["prod-123", "prod-456"],
  "discount_percent": 30,
  "target_audience": "all",
  "start_date": "2024-06-01T00:00:00Z",
  "end_date": "2024-08-31T23:59:59Z"
}
```

**Response:**
```json
{
  "id": "promo-abc-123",
  "name": "Summer Sale 2024",
  "status": "active",
  "conversions": 0,
  "revenue": 0.0,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Get Promotion Performance
```bash
GET /promotions/{promotion_id}/performance
```

**Response:**
```json
{
  "promotion_id": "promo-abc-123",
  "name": "Summer Sale 2024",
  "conversions": 1250,
  "revenue": 124500.00,
  "discount_percent": 30,
  "roi": 450.5,
  "status": "active",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Product Bundles (L20 Tier)

#### Create Bundle
```bash
POST /bundles
Content-Type: application/json

{
  "name": "Enterprise AI Bundle",
  "description": "Complete AI solution for enterprises",
  "product_ids": ["ai-gen-1", "bot-orchestration", "analytics-pro"],
  "bundle_price": 9999.99,
  "discount_percent": 25,
  "tier": "L20",
  "customization_options": {
    "custom_branding": true,
    "dedicated_support": true,
    "sla_99_9": true
  }
}
```

**Response:**
```json
{
  "id": "bundle-xyz-789",
  "name": "Enterprise AI Bundle",
  "tier": "L20",
  "product_ids": ["ai-gen-1", "bot-orchestration", "analytics-pro"],
  "bundle_price": 9999.99,
  "discount_percent": 25,
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Dashboard Management

#### Request Dashboard Change
```bash
POST /dashboard/change-request
Content-Type: application/json

{
  "requested_by": "user-123",
  "owner_id": "owner-456",
  "change_type": "metrics",
  "priority": "high",
  "changes": {
    "add_widgets": ["conversion_rate", "revenue_chart"],
    "remove_widgets": ["old_metric_1"]
  }
}
```

**Response:**
```json
{
  "id": "change-request-abc",
  "status": "pending_approval",
  "requested_by": "user-123",
  "priority": "high",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Approve Dashboard Change (Owner Only)
```bash
POST /dashboard/approve/{request_id}
Content-Type: application/json

{
  "approver_id": "owner-456"
}
```

#### Rollback Dashboard
```bash
POST /dashboard/rollback
Content-Type: application/json

{
  "config_id": "config-xyz-123"  # Optional: specific config to rollback to
}
```

#### Get Pending Approvals
```bash
GET /dashboard/pending-approvals
```

**Response:**
```json
{
  "pending_approvals": [
    {
      "id": "change-request-abc",
      "status": "pending_approval",
      "priority": "high",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

### Analytics

#### Get Marketing Analytics
```bash
GET /analytics?timeframe=30d
```

**Response:**
```json
{
  "total_promotions": 50,
  "active_promotions": 12,
  "total_conversions": 5000,
  "revenue_generated": 500000.00,
  "total_products": 100,
  "total_bundles": 15,
  "pending_approvals": 3,
  "timeframe": "30d",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Usage Examples

### Create L20 Enterprise Bundle
```python
import requests

bundle_data = {
    "name": "Ultimate AI Suite",
    "description": "Complete AI platform",
    "product_ids": ["ai-chat", "ai-gen", "bot-swarm"],
    "bundle_price": 19999.99,
    "discount_percent": 30,
    "tier": "L20",
    "customization_options": {
        "white_label": True,
        "custom_training": True,
        "24_7_support": True
    }
}

response = requests.post('http://localhost:5007/bundles', json=bundle_data)
bundle = response.json()
print(f"Created bundle: {bundle['id']}")
```

### Track Promotion Performance
```python
import requests

# Get performance metrics
response = requests.get('http://localhost:5007/promotions/promo-123/performance')
performance = response.json()

print(f"Conversions: {performance['conversions']}")
print(f"Revenue: ${performance['revenue']}")
print(f"ROI: {performance['roi']}%")
```

### Dashboard Change with Approval
```python
import requests

# Request change
change_request = {
    "requested_by": "marketing-team",
    "owner_id": "business-owner",
    "change_type": "layout",
    "priority": "high",
    "changes": {
        "new_layout": "revenue_focused",
        "add_kpis": ["conversion_rate", "ltv"]
    }
}

response = requests.post('http://localhost:5007/dashboard/change-request', 
                        json=change_request)
request_id = response.json()['id']

# Owner approves
approval = {
    "approver_id": "business-owner"
}

response = requests.post(f'http://localhost:5007/dashboard/approve/{request_id}',
                        json=approval)
print(f"Change approved: {response.json()['status']}")
```

## L20 Orchestration Features

The L20 tier provides advanced capabilities for enterprise customers:

- **Mass-customized promotions** - Scale to millions of users
- **Dynamic product bundling** - Real-time bundle optimization
- **Advanced analytics** - Deep insights and predictive modeling
- **Priority support** - Dedicated account management
- **Custom integrations** - Tailored to business needs
- **Dashboard rollback** - Owner approval priority for safety

## Configuration

Environment variables:
- `LOG_LEVEL` - Logging level (default: info)

## Docker

```bash
# Build
docker build -t marketing-intelligence-service .

# Run
docker run -p 5007:5007 marketing-intelligence-service
```

## Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "marketing-intelligence",
  "timestamp": "2024-01-01T00:00:00Z"
}
```
