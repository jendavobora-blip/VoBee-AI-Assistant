Add final MVP README
# VoBee AI Assistant

VoBee je **hotová PWA aplikace** (web + mobil), která funguje jako osobní AI asistent zaměřený na:
- finance
- kryptoměny
- běžné denní otázky
- rychlé rozhodování
- jednoduché plánování

Aplikace je navržená tak, aby:
- byla **okamžitě použitelná**
- šla **nainstalovat do telefonu**
- fungovala **bez složité infrastruktury**
- byla **rozšiřitelná do budoucna**

---

## 📱 Instalace (iPhone / Android / PC)

### iPhone (Safari)
1. Otevři aplikaci v Safari
2. Klikni na **Sdílet**
3. Zvol **Přidat na plochu**
4. Hotovo – aplikace se chová jako nativní

### Android (Chrome)
1. Otevři aplikaci
2. Zvol **Install app**
3. Hotovo

### PC / Mac
- Aplikaci lze spustit jako PWA přímo z prohlížeče

---

## ✅ Aktuální MVP funkce

- 🧠 Chat AI asistenta
- 💬 Textová konverzace
- 💾 Lokální paměť (IndexedDB / localStorage)
- ⚡ Rychlá odezva
- 📱 Plná podpora mobilu
- 🌐 Offline-ready základ

---

## 🚧 Co je záměrně jednoduché (MVP)

- Žádné účty
- Žádné přihlašování
- Žádný backend server
- Žádná automatická „superinteligence“

➡️ Cílem MVP je **funkční aplikace**, ne marketingový slib.

---

## 🛣️ Plán dalšího rozvoje (ne teď)

- Hlasový vstup / výstup
- Lepší paměť konverzací
- Personalizace odpovědí
- Rozšíření finančních scénářů
- Napojení externích API (volitelné)

Tyto věci **nejsou součástí MVP** a budou řešeny až po stabilní verzi.

---

## 🚀 Vobio AI Studio - Production-Ready Platform

**Nová verze** s kompletní produkční infrastrukturou!

### Quick Start (One-Command Setup)

```bash
# Clone repository
git clone https://github.com/jendavobora-blip/VoBee-AI-Assistant.git
cd VoBee-AI-Assistant

# Setup everything
./setup.sh

# Start all services
./start.sh

# Run tests
./test.sh
```

### Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Vobio API** | http://localhost:8000 | Main API server |
| **API Health** | http://localhost:8000/health | Health check |
| **Langfuse** | http://localhost:3000 | Observability dashboard |
| **Qdrant** | http://localhost:6333 | Vector database |
| **OTEL Collector** | http://localhost:4317 | Telemetry (gRPC) |

### Features

✅ **Complete Runtime Contract**
- 🎯 OpenFeature (Feature Flags)
- 🔄 LangGraph (AI Orchestration)
- 📊 Langfuse (Observability & Cost Tracking)
- 🔍 OpenTelemetry (Distributed Tracing)
- 🗄️ Qdrant (Vector Memory)
- 🔐 Passkey Identity (Mock Mode)

✅ **Safety System**
- Code validation & sandboxing
- Protected file system
- Cost limits ($10/day, $2/hour)
- Human approval workflow
- Automatic quarantine

✅ **AI Capabilities** (Mock Mode)
- Chat assistant
- Image generation
- Video generation
- LifeSync decision assistant

✅ **Production Ready**
- Docker Compose infrastructure
- Automated setup/start/test scripts
- Health checks & monitoring
- Comprehensive documentation

### LifeSync Decision Assistant Example

```bash
curl -X POST http://localhost:8000/api/lifesync/decision \
  -H "X-User-ID: user123" \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "Should I change jobs?",
    "options": ["Stay", "New startup", "Freelance"],
    "user_context": {"priority": "financial"}
  }'
```

### Documentation

- 📖 [Architecture Guide](vobio-ai-studio/ARCHITECTURE.md) - System design & components
- 🔒 [Safety Guide](vobio-ai-studio/SAFETY.md) - Security & safety systems
- 📡 [API Reference](vobio-ai-studio/API.md) - Complete API documentation

### Troubleshooting

**Services won't start:**
```bash
# Check Docker status
docker ps

# View logs
docker-compose -f vobio-ai-studio/docker-compose.yml logs

# Reset everything
./stop.sh
docker-compose -f vobio-ai-studio/docker-compose.yml down -v
./setup.sh
./start.sh
```

**Tests failing:**
```bash
# Wait longer for services to start
sleep 30 && ./test.sh

# Check individual service health
curl http://localhost:8000/health
curl http://localhost:6333/health
curl http://localhost:3000/api/health
```

**Port conflicts:**
Edit `vobio-ai-studio/docker-compose.yml` and change port mappings.

### Requirements

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB disk space

### Stop Services

```bash
./stop.sh
```

---

## 👤 Autor

**Jan Vobora**  
Projekt VoBee

---

## ⚠️ Poznámka

Tento repozitář obsahuje:
1. **Původní PWA MVP** - Jednoduchá aplikace pro okamžité použití
2. **Vobio AI Studio** - Kompletní produkční platforma s full-stack infrastrukturou

Obě verze jsou **plně funkční** a připravené k použití.

---