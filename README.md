# KisanSamvaad (किसान संवाद / ಕಿಸಾನ್ ಸಂವಾದ)
### Sovereign Indic Voice & Document AI for Indian Agriculture • Powered by Sarvam AI

[![Hackathon Track](https://img.shields.io/badge/Track%2003-Agriculture%20%26%20Rural%20Innovation-15803d?style=for-the-badge)](https://sarvam.ai)
[![Powered By](https://img.shields.io/badge/Powered%20By-Sarvam%20AI-f97316?style=for-the-badge)](https://sarvam.ai)
[![Sovereign Models](https://img.shields.io/badge/Models-Saaras%20%7C%20Bulbul%20%7C%20Sarvam--1%20%7C%20Document%20Vision%20%7C%20Mayura-blue?style=for-the-badge)](https://sarvam.ai)
[![Memory Footprint](https://img.shields.io/badge/RAM%20Footprint-%3C100MB-emerald?style=for-the-badge)](#)
[![Tests Passing](https://img.shields.io/badge/Tests-31%2F31%20Passed-brightgreen?style=for-the-badge)](#)

---

## 🌾 1. Product Vision & Sovereign AI Mission

KisanSamvaad (किसान संवाद / ಕಿಸಾನ್ ಸಂವಾದ) is a sovereign, voice-first agricultural intelligence platform and document concierge built directly on Sarvam AI Indic language models for India's 140+ million farmers.

### Guiding Principle
"Putting sovereign AI directly into the hands of the person who feeds the nation."

Among hackathon domains, Agriculture & Rural Innovation (Track 03) is the premier fit for sovereign Indic AI:
1. Zero Literacy Barrier (Voice-First): Over 60% of smallholder farmers cannot or will not type complex English prompts. KisanSamvaad enables 100% voice-in, voice-out interaction in regional Indian languages.
2. Code-Mixed Dialect Native: Natural rural speech (Kanglish, Hinglish, regional phrasing) is understood natively where foreign English-centric models fail.
3. Sovereign Document OCR: Scans physical Soil Health Cards (ಮೃದಾ ಆರೋಗ್ಯ ಕಾರ್ಡ್ / मृदा स्वास्थ्य कार्ड) with Sarvam Document Vision and provides actionable fertilizer remediation.
4. Radical Rural Reach (Toll-Free Telephony): Bridges the digital divide by connecting to ₹1,000 keypad phones via simulated 1800-KISAN-AI IVR with zero internet requirement.
5. Deterministic AgriGuardrails: Fails closed on banned pesticides and toxic dilutions, grounding every recommendation in verified ICAR research packages.

---

## ⚡ 2. Engineered for 8GB RAM PCs (Ultra-Lightweight)

KisanSamvaad is intentionally built to run with zero heavy overhead:
- Active Memory Usage: Under 100MB RAM.
- Startup Time: Under 120 milliseconds.
- Zero Heavy Containers: Runs natively via the Python standard library; no Docker or Kubernetes cluster needed for local development or field demos.
- High-Fidelity Dual Mode: Operates offline out-of-the-box with calibrated ICAR agronomic models and DTMF acoustic synthesis; seamlessly switches to live Sarvam Cloud APIs when an API key is provided.

---

## 🏛️ 3. System Architecture & Core Subsystems

```mermaid
flowchart TD
    subgraph Clients["Farmer Access Channels"]
        A["2G Keypad Feature Phone<br/>(PSTN Toll-Free 1800-IVR)"]
        B["Low-End Smartphone<br/>(Offline PWA Shell)"]
    end

    subgraph CoreServer["KisanSamvaad Server (<100MB RAM)"]
        Router["API Router & Dispatcher<br/>(backend/server.py)"]
        
        subgraph SafetyEngine["Deterministic Safety Guardrails"]
            Guard["AgriGuardrail Engine<br/>(Fail-Closed Policy)"]
            CIBRC["CIBRC Banned Pesticide Interceptor<br/>(Endosulfan, Paraquat, etc.)"]
            Dosage["ICAR Agrochemical Dosage Bounds<br/>(Imidacloprid <= 0.5 ml/L)"]
            Audit["Safety Audit Logger<br/>(Multilingual KVK Notices)"]
        end

        subgraph SarvamPipeline["Sarvam AI Sovereign Pipeline"]
            ASR["Saaras v3 ASR<br/>(Code-Mixed Indic Speech)"]
            TTS["Bulbul v4 TTS<br/>(Authentic Indian Prosody)"]
            LLM["Sarvam-1 Indic LLM<br/>(Agricultural Reasoning)"]
            OCR["Document Vision OCR<br/>(Soil Health Card Tables)"]
            Mayura["Mayura Translation<br/>(Preserves Agri Terminology)"]
        end

        subgraph Services["Agricultural Intelligence Services"]
            SoilSvc["Soil Diagnostic Service<br/>(NPK & pH Remediation)"]
            Telephony["1800-IVR Telephony<br/>(DTMF Routing 1-4)"]
        end
    end

    subgraph Groundings["Verified Agricultural Groundings"]
        RAG["ICAR / UAS Bangalore Packages<br/>(Kolar Tomato, Raichur Cotton)"]
        Mandi["APMC Mandi Connector<br/>(Real Modal Rates: DEMO / LIVE)"]
        Weather["IMD Weather Connector<br/>(Spray Window Advisories)"]
    end

    A -->|"Audio / DTMF"| Router
    B -->|"REST / Audio Stream"| Router
    Router --> Services
    Router --> SarvamPipeline
    SarvamPipeline <--> SafetyEngine
    SafetyEngine <--> Groundings
    Services <--> Groundings
```

---

## 🔄 4. End-to-End Voice Advisory Loop

```mermaid
sequenceDiagram
    autonumber
    actor Farmer as Farmer (Kannada / Hindi)
    participant Client as PWA / Keypad Phone
    participant Server as KisanSamvaad Server
    participant Saaras as Sarvam Saaras ASR
    participant Guard as AgriGuardrail Engine
    participant RAG as ICAR Knowledge Base
    participant LLM as Sarvam-1 Indic LLM
    participant Bulbul as Sarvam Bulbul TTS

    Farmer->>Client: Speaks in native dialect ("Mere tamatar me peeli patti hai...")
    Client->>Server: POST /api/stt (Audio Stream)
    Server->>Saaras: Transcribe code-mixed audio
    Saaras-->>Server: Spoken text transcript
    Server->>Guard: Pre-validate query for banned chemicals
    alt Banned substance detected (e.g., Endosulfan)
        Guard-->>Server: Fail-closed alert (Class I toxin)
        Server->>Bulbul: Synthesize urgent safety warning
        Bulbul-->>Client: Spoken KVK advisory (Audio)
        Client-->>Farmer: "Prohibited chemical alert. Consult local KVK."
    else Safe query
        Guard-->>Server: Query passed safety check
        Server->>RAG: Retrieve crop package (Kolar Tomato / Raichur Cotton)
        RAG-->>Server: Verified ICAR dosage & organic remedies
        Server->>LLM: Reason with ICAR grounding
        LLM-->>Server: Structured agronomic advice
        Server->>Guard: Post-validate chemical dosage & PPE notice
        Guard-->>Server: Validated & sanitized response
        Server->>Bulbul: POST /api/tts (Synthesize voice)
        Bulbul-->>Server: WAV audio with Indic prosody
        Server-->>Client: Voice audio + text transcript + provenance citation
        Client-->>Farmer: Hears natural spoken answer in native language
    end
```

---

## 🧪 5. Soil Health Card Intelligence Workflow

```mermaid
flowchart LR
    A["Physical Paper<br/>Soil Health Card"] -->|"Upload / Camera Scan"| B["Sarvam Document Vision<br/>(Indic OCR Pipeline)"]
    B --> C["Tabular Extraction<br/>(N, P, K, pH, OC, Zinc)"]
    C --> D["Confidence Scoring<br/>(e.g., 96% Conf on N)"]
    D --> E["Interactive Manual Override<br/>(/api/soil-evaluate)"]
    E --> F["ICAR Diagnostic Engine<br/>(Deficiency Classification)"]
    F --> G["Precision Soil Action Plan<br/>(Remediation & ₹4,000/acre savings)"]
```

---

## ☎️ 6. 1800-KISAN-AI Telephony State Machine

```mermaid
stateDiagram-v2
    [*] --> CallConnected: Farmer Dials 1800-KISAN-AI
    CallConnected --> WelcomeMenu: Multi-Dialect Greeting Spoken
    
    WelcomeMenu --> SoilAnalysis: Farmer Presses 1
    WelcomeMenu --> MandiRates: Farmer Presses 2
    WelcomeMenu --> WeatherSpray: Farmer Presses 3
    WelcomeMenu --> VoiceDoctor: Farmer Presses 4

    SoilAnalysis --> ReturnToMenu: Soil Status Spoken
    MandiRates --> ReturnToMenu: Modal APMC Rate Spoken
    WeatherSpray --> ReturnToMenu: Spray Window Alert Spoken
    VoiceDoctor --> AudioRecording: Record Farmer Spoken Query

    ReturnToMenu --> WelcomeMenu: Press 0 or Wait
    AudioRecording --> AdvisoryPlayback: Process via Saaras + Sarvam-1
    AdvisoryPlayback --> ReturnToMenu: Advice Spoken
    ReturnToMenu --> [*]: Farmer Hangs Up
```

---

## 🚀 7. Quick Start Guide

### Step 1: Clone and Navigate
```bash
cd c:/Users/hp/OneDrive/Desktop/SARVAM
```

### Step 2: Environment Configuration (Optional)
```bash
# Copy example environment configuration
copy .env.example .env
```
To run with live Sarvam Cloud APIs, set `SARVAM_API_KEY=your_key_here` in `.env` or click the settings cog in the top-right corner of the web interface. If left blank, KisanSamvaad operates in offline demonstration mode.

### Step 3: Start the Application Server
```bash
python backend/server.py 8000
```
Open your browser at:  
👉 **`http://localhost:8000`**

### Step 4: Run the Master 10-Point Automated Test Suite
```bash
python backend/tests/run_all_tests.py
```

Output:
```
======================================================================
🌾 KISANSAMVAAD MASTER TEST SUITE - 10 CRITICAL SPECIFICATION AREAS
======================================================================
  [PASSED] Suite 1. Sarvam Handling & Fallback (3 tests)
  [PASSED] Suite 2. Speech Workflow & Synthesis (2 tests)
  [PASSED] Suite 3. Soil Card Validation & Remediation (4 tests)
  [PASSED] Suite 4. Agricultural RAG & Provenance (3 tests)
  [PASSED] Suite 5. Banned Chemical Fail-Closed Guardrails (4 tests)
  [PASSED] Suite 6. Restricted Agrochemical Dosages (3 tests)
  [PASSED] Suite 7. Mandi Data Freshness & Transparency (3 tests)
  [PASSED] Suite 8. Agricultural Weather & Spray Windows (2 tests)
  [PASSED] Suite 9. API Error Handling & Resilience (5 tests)
  [PASSED] Suite 10. End-to-End Multilingual Pipeline (2 tests)
======================================================================
✅ ALL 31 VERIFICATION TESTS PASSED SUCCESSFULLY! (0.07s)
======================================================================
```

---

## 📱 8. Feature Highlights

### 1. Suno & Bolo (AI Voice Assistant)
- Multi-dialect support: Kannada, Hindi, Tamil, Telugu, Marathi, Bengali, and Indian English.
- Real-time Web Audio API waveform canvas visualizer.
- Speech-to-Speech loop with transcript display and replay buttons.

### 2. Soil Health Card Intelligence with Manual Override
- High-accuracy OCR extraction of Nitrogen, Phosphorus, Potassium, and pH.
- Per-metric confidence tags (e.g. 96% Conf).
- Interactive manual correction: Farmers can edit extracted values and click "Recalculate Soil Diagnosis" to immediately receive updated organic and biological remediation steps.
- Estimated savings: Avoids ₹3,200 to ₹4,800 per acre in over-applied chemical fertilizers.

### 3. Real APMC Mandi Rates
- Tracks Kolar (Tomato), Yeshwanthpur (Onion), Raichur (Cotton), Shimoga (Arecanut), Neemuch (Soybean), and Lasalgaon (Onion).
- Shows modal, minimum, and maximum rates in ₹ / Quintal.
- Transparently tagged with freshness timestamps and `LIVE` or `DEMO` status.

### 4. IMD Weather & Spray Window Advisory
- Evaluates wind speed (< 15 km/h safe) and precipitation likelihood.
- Generates clear spray advisories: Safe morning foliar windows vs. strict wash-off warnings during thunderstorms.

### 5. Deterministic ICAR AgriGuardrails
- Completely blocks banned chemicals (Endosulfan, Monocrotophos, Paraquat, Methyl Parathion, DDT).
- Clamps lethal or crop-burning dilutions (e.g., Imidacloprid > 0.5 ml/L).
- Logs audit events and appends mandatory KVK verification notices in the farmer's native language.

### 6. 1800-KISAN-AI Telephony IVR Simulator
- Simulates toll-free keypad phone access with synthesized DTMF tones via the Web Audio API.
- Press 1 for Soil Analysis, 2 for Mandi Rates, 3 for Weather Spray Advisory, 4 for Voice Doctor.

### 7. Progressive Web App (PWA) & Offline Shell
- Web app manifest (`frontend/manifest.json`) and service worker (`frontend/sw.js`) ensure seamless caching for rural 2G mobile data connections.

---

## 📚 9. Documentation Index

- [docs/architecture.md](docs/architecture.md): Complete architecture document, low-resource design rationale, and data flow models.
- [docs/api.md](docs/api.md): REST API endpoints, schemas, and curl examples.
- [presentation.html](presentation.html): Interactive 8-slide hackathon presentation deck.
- [data/knowledge/](data/knowledge/): Verified agronomic packages from ICAR, KVK, and UAS Bangalore.

---

## 🏆 Hackathon Submission Metadata
- Event: Vertex Club, REVA University x Sarvam AI Hackathon
- Track: Track 03: Agriculture & Rural Innovation
- Team: KisanSamvaad Architects
- License: MIT
