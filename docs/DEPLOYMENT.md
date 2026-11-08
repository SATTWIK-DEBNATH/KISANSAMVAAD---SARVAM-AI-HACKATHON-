# KisanSamvaad - Deployment & Operations Guide
## Sovereign Indic Voice and Document AI for Indian Agriculture

Date: November 2026  
Status: Production Operations Manual  
DevOps Lead: Principal Infrastructure Architect  

---

## 1. System Requirements & Hardware Sizing

KisanSamvaad is engineered to run on standard consumer hardware and low-resource rural computers without requiring specialized GPUs or cloud orchestration.

### Supported Target Environments:
- Rural Extension Kiosk / KVK Desktop: Windows 10/11 or Ubuntu Desktop (4GB to 8GB RAM, Core i3 or Ryzen 3).
- Embedded Edge Server: Raspberry Pi 4 / 5 (4GB RAM) running Raspberry Pi OS (Debian).
- Production Cloud Instance: AWS t3.small, Azure B1ms, or Google Cloud e2-micro (1 vCPU, 1GB to 2GB RAM).

### Resource Consumption Profile:
- Active RAM Usage: 45MB to 75MB.
- Disk Footprint: <20MB for application runtime; ~5MB per 10,000 farmer consultation records in SQLite.
- CPU Utilization: <2% on idle; bursts to 15% during active audio base64 decoding.

---

## 2. Bare-Metal Deployment (Windows / Linux / macOS)

### Step 1: Clone Repository
```bash
git clone <repository_url>
cd SARVAM
```

### Step 2: Configure Environment (Optional)
Copy the template configuration file:
```bash
cp .env.example .env
```
To enable live Sarvam AI sovereign cloud models, set your API key in `.env`:
```text
SARVAM_API_KEY=your_actual_sarvam_key_here
```
Note: If `SARVAM_API_KEY` is omitted, KisanSamvaad starts automatically in calibrated offline ICAR simulation mode.

### Step 3: Run Master Test Suite Verification
Before starting the server, run the automated verification suite:
```bash
python backend/tests/run_all_tests.py
```
Ensure all 14 suites pass successfully.

### Step 4: Start the Server
On Windows:
```powershell
python backend/server.py 8000
```
Or use the convenience startup scripts:
```powershell
.\run_demo.ps1
```

On Linux / macOS:
```bash
python3 backend/server.py 8000
```

### Step 5: Access Web Client
Open any modern web browser (Google Chrome, Firefox, Safari, Edge) to:
```text
http://127.0.0.1:8000
```

---

## 3. Containerized Deployment (Docker & Docker Compose)

Containerization isolates dependencies and simplifies cloud or multi-node deployment.

### Option A: Running with Docker Compose (Recommended)
Launch the application with automatic persistent data volumes and resource limits:
```bash
# Build and start in detached mode
docker compose up -d --build

# View real-time container logs
docker compose logs -f

# Check container health status
docker compose ps
```

The container automatically enforces resource boundaries:
- CPU limit: 1.0 core.
- Memory limit: 256MB.
- Memory reservation: 64MB.

### Option B: Building and Running Bare Docker Container
```bash
# Build Docker image
docker build -t kisansamvaad:latest .

# Run container with volume mount for SQLite persistence
docker run -d \
  --name kisansamvaad_ai \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e SARVAM_API_KEY=your_sarvam_key \
  kisansamvaad:latest
```

---

## 4. Health Check & Diagnostic Verification

Verify operational health using `curl` or PowerShell:

```bash
curl -s http://127.0.0.1:8000/api/health
```

Expected JSON response:
```json
{
  "status": "healthy",
  "service": "KisanSamvaad Sovereign Agricultural AI",
  "version": "2.4.0",
  "sarvam_live_connected": false,
  "supported_languages": [
    {"code": "kn-IN", "name": "Kannada (ಕನ್ನಡ) - Primary Regional Focus"},
    {"code": "hi-IN", "name": "Hindi (हिंदी)"},
    {"code": "ta-IN", "name": "Tamil (தமிழ்)"},
    {"code": "te-IN", "name": "Telugu (తెలుగు)"},
    {"code": "en-IN", "name": "Indian English"}
  ]
}
```

---

## 5. Troubleshooting & Operational Runbook

1. Port 8000 Already in Use:
   - Identify blocking process: `netstat -ano | findstr :8000` (Windows) or `lsof -i :8000` (Linux).
   - Start KisanSamvaad on an alternative port: `python backend/server.py 8080`.
2. Database Lock Contention:
   - KisanSamvaad enables SQLite Write-Ahead Logging (`PRAGMA journal_mode=WAL;`) and busy timeouts (`PRAGMA busy_timeout=5000;`) to prevent concurrency locks across multiple threads.
3. Audio Playback Muted on Mobile Browsers:
   - Mobile browsers (Safari on iOS, Chrome on Android) require user interaction (a tap on the screen) before playing synthetic audio via the HTML5 Web Audio API. Ensure the farmer presses the microphone or speaker icon before expecting audio output.
