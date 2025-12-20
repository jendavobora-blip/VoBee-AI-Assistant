# What is Functional - Protected Components

## ⚠️ CRITICAL: DO NOT MODIFY THESE FILES

This document lists all working components that **MUST NOT** be modified, deleted, or broken.

## 🔒 Protected Files & Services

### Core Services (DO NOT TOUCH)

#### 1. `/services/orchestrator/main.py`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Main orchestration engine
- **Why Protected**: Core task coordination and workflow management
- **Lines of Code**: 402
- **Dependencies**: Redis, PostgreSQL, all AI services

#### 2. `/services/api-gateway/main.py`
- **Status**: ✅ FUNCTIONAL  
- **Purpose**: Main API entry point
- **Why Protected**: All external requests go through this gateway

#### 3. `/services/image-generation/main.py`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Image generation with Stable Diffusion
- **Why Protected**: Working GPU-accelerated service

#### 4. `/services/video-generation/main.py`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Video generation with NeRF/Runway
- **Why Protected**: Working GPU-accelerated service

#### 5. `/services/crypto-prediction/main.py`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Cryptocurrency price prediction
- **Why Protected**: Real-time market analysis

#### 6. `/services/fraud-detection/main.py`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Fraud detection and prevention
- **Why Protected**: Security-critical service

#### 7. `/services/supreme-general-intelligence/main.py`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Main AI interface and intent understanding
- **Why Protected**: User-facing intelligence layer

#### 8. `/services/spy-orchestration/main.py`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: GitHub repository discovery and analysis
- **Why Protected**: Autonomous discovery system

#### 9. `/services/self-healing/main.py`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Auto-repair and health monitoring
- **Why Protected**: System reliability

#### 10. `/services/worker-pool/main.py`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Worker management and task execution
- **Why Protected**: Task distribution system

#### 11. `/services/auto-scaler/main.py`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Dynamic scaling based on load
- **Why Protected**: Performance optimization

#### 12. `/services/cdn/main.py`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Content delivery and caching
- **Why Protected**: Performance and availability

### Frontend Files (DO NOT TOUCH)

#### 1. `/js/chatbot.js`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Main chatbot interface
- **Why Protected**: User interaction layer
- **Features**: Pattern matching, IndexedDB, conversation history

#### 2. `/js/response-patterns.js`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Response pattern library
- **Why Protected**: Chatbot intelligence

#### 3. `/index.html`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Main web interface
- **Why Protected**: User interface

#### 4. `/sw.js`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Service worker for PWA
- **Why Protected**: Offline capability

### Configuration Files (MODIFY WITH EXTREME CAUTION)

#### 1. `/docker-compose.yml`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Container orchestration
- **Modification Rule**: **ONLY ADD**, never remove or change existing services
- **Current Services**: 18 services running

#### 2. `/kubernetes/01-deployments.yaml`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Kubernetes deployments
- **Modification Rule**: **ONLY ADD**, never remove or change existing deployments

#### 3. `/kubernetes/02-infrastructure.yaml`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Infrastructure components
- **Why Protected**: Redis, PostgreSQL, Elasticsearch, Kibana

#### 4. `/kubernetes/03-autoscaling.yaml`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: HPA configurations
- **Why Protected**: Auto-scaling rules

#### 5. `/kubernetes/00-namespace-config.yaml`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: Namespace and config
- **Why Protected**: Cluster configuration

### Database & Storage (DO NOT TOUCH)

#### PostgreSQL
- **Database**: `orchestrator_db`
- **User**: `orchestrator`
- **Purpose**: Persistent data storage
- **Status**: ✅ FUNCTIONAL

#### Redis
- **Purpose**: Task queue and caching
- **Status**: ✅ FUNCTIONAL

#### Elasticsearch
- **Purpose**: Logging and search
- **Status**: ✅ FUNCTIONAL

### Scripts & Automation (DO NOT TOUCH)

#### 1. `/test-system.sh`
- **Status**: ✅ FUNCTIONAL
- **Purpose**: System integration testing
- **Tests**: 12 test cases
- **Why Protected**: Validation framework

#### 2. `/deploy.sh`
- **Status**: ✅ FUNCTIONAL (if exists)
- **Purpose**: Deployment automation
- **Why Protected**: Production deployment

### Documentation (DO NOT DELETE)

#### Existing Documentation
- `/ARCHITECTURE.md` - System architecture
- `/AUTONOMOUS_SYSTEM.md` - Autonomous features
- `/DEPLOYMENT.md` - Deployment guide
- `/IMPLEMENTATION_SUMMARY.md` - Implementation details
- `/QUICKSTART.md` - Quick start guide
- `/VALIDATION_CHECKLIST.md` - Validation steps
- `/README.md` - Main documentation

**Rule**: Can be extended, but not deleted or restructured

## ✅ How to Extend Without Breaking

### Adding New Services
```yaml
# In docker-compose.yml
# ✅ CORRECT: Add new service at the end
  new-service:
    build: ./services/new-service
    ports:
      - "5999:5000"
    networks:
      - ai-network

# ❌ WRONG: Don't modify existing services
  orchestrator:  # DON'T CHANGE THIS
    build: ./services/orchestrator
```

### Adding New Orchestrator Features
```python
# ✅ CORRECT: Create new module
# /services/orchestrator/new-feature.py
class NewFeature:
    def process(self):
        # New functionality
        pass

# ❌ WRONG: Don't modify main.py
# /services/orchestrator/main.py (DON'T EDIT)
```

### Adding Frontend Features
```javascript
// ✅ CORRECT: Create new file
// /js/new-feature.js
class NewFeature {
  // New functionality
}

// ❌ WRONG: Don't modify chatbot.js
// /js/chatbot.js (DON'T EDIT)
```

## 🔍 What CAN Be Modified

### Safe to Add
- ✅ New services in `/services/`
- ✅ New modules in `/services/orchestrator/`
- ✅ New JavaScript files in `/js/`
- ✅ New documentation in `/docs/`
- ✅ New tests in `/tests/`
- ✅ New configuration in `/config/`
- ✅ New monitoring in `/monitoring/`

### Safe to Extend
- ✅ Add entries to `docker-compose.yml`
- ✅ Add deployments to Kubernetes YAML files
- ✅ Add new environment variables (`.env.example`)
- ✅ Add new dependencies to new services
- ✅ Add new API endpoints to new services

## 🚫 What CANNOT Be Modified

### Never Touch
- ❌ Existing service `main.py` files
- ❌ Existing JavaScript files
- ❌ Existing HTML files
- ❌ Existing database schemas
- ❌ Existing Docker networks
- ❌ Existing Kubernetes namespaces
- ❌ Existing service ports (use new ports for new services)

### Never Delete
- ❌ Any existing service
- ❌ Any existing endpoint
- ❌ Any existing configuration
- ❌ Any existing documentation

### Never Break
- ❌ Existing APIs
- ❌ Existing workflows
- ❌ Existing tests
- ❌ Existing integrations

## 📊 Testing Protected Components

Before any deployment, verify all protected components still work:

```bash
# Run integration tests
./test-system.sh

# Expected: All 12 tests should pass
# ✅ API Gateway health
# ✅ SGI service health
# ✅ Spy-Orchestration health
# ✅ Self-Healing health
# ✅ Worker Pool health
# ✅ System health summary
# ✅ SGI chat interface
# ✅ Worker pool status
# ✅ Worker creation
# ✅ Worker task execution
# ✅ Spy stats
# ✅ Orchestrator health
```

## 🎯 Summary Rules

1. **NEVER** modify files listed in "Protected Files & Services"
2. **ALWAYS** create new files instead of editing existing ones
3. **ONLY ADD** to docker-compose.yml and Kubernetes files
4. **EXTEND** functionality by wrapping, not replacing
5. **TEST** that all protected components still work after changes

---

## 🚨 Emergency Recovery

If protected components are accidentally modified:

1. **Stop immediately**
2. **Restore from git**: `git checkout HEAD -- <file>`
3. **Run tests**: `./test-system.sh`
4. **Verify**: Check all services are healthy
5. **Document**: What was attempted and why it failed

---

*Remember: NAVAZUJ, NENIČ (Build Upon, Never Destroy)*

*Last Updated: 2024-01-20*
