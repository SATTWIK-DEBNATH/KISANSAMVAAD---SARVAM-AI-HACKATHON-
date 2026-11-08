# KisanSamvaad System Architecture Specification

## 1. Executive Summary & Framework Decision

### Architectural Decision
In accordance with Brief Section 3.2 ("If the project is not React, keep its framework and apply the same architecture principles. Record the decision and reasons in ARCHITECTURE.md"), KisanSamvaad implements a **Static-First, Hybrid Micro-Engine Architecture** powered by standard web primitives (HTML5, Vanilla ES6+ TypeScript/JavaScript, CSS Variables) served by an ultra-lightweight Python backend.

### Evaluation & Rationale
1. **Zero Hydration Latency on Low-End Devices**:
   - Rural Indian farmers predominantly access digital services on entry-level Android smartphones with 2GB to 3GB RAM over fluctuating 2G/3G/4G connections.
   - Traditional Single-Page Applications (Next.js/React) require multi-megabyte JavaScript bundles, virtual DOM reconciliation, and heavy runtime hydration that stalls the main thread.
   - KisanSamvaad achieves First Contentful Paint (FCP) under 350ms and complete Time to Interactive (TTI) under 600ms by shipping pure semantic HTML and self-contained CSS tokens.
2. **Deterministic Offline Capability**:
   - The platform operates completely offline when disconnected, serving cached agricultural knowledge packages, synthetic Soil Health Cards, and client-side speech synthesis fallbacks via Web Speech API and Service Workers.
3. **Hardware-Efficient Execution (<100MB RAM)**:
   - The backend runs entirely on Python standard library socket and HTTP servers without external framework bloat (FastAPI/Node), making it deployable on ₹1,000 edge gateways or low-spec hardware.

---

## 2. Dual-Surface System Architecture

The platform provides two deeply integrated surfaces sharing identical design tokens and data contracts:

```
+---------------------------------------------------------------------------------------+
|                                    KISANSAMVAAD CORE                                  |
|                                                                                       |
|   +---------------------------------------+   +-----------------------------------+   |
|   |       SURFACE 1: EDITORIAL SITE       |   |      SURFACE 2: FARMER APP        |   |
|   |   (Cinematic Landing & Storytelling)  |   |   (9 Farmer Task-Oriented Screens)|   |
|   +---------------------------------------+   +-----------------------------------+   |
|                       |                                         |                     |
|                       +--------------------+--------------------+                     |
|                                            |                                          |
|                                            v                                          |
|                         [ SHARED DESIGN SYSTEM & TOKENS ]                             |
|                           - Space Grotesk / Inter / Indic                             |
|                           - Deep Forest Green / Amber / Sage                          |
|                           - Tactile Grain & Hairline Grids                            |
|                           - Truthful Data Provenance Tag                              |
|                                            |                                          |
|                                            v                                          |
|                         [ SOVEREIGN INDIC SERVICE WORKER ]                            |
|                           - Offline Cache Storage                                     |
|                           - PWA Application Manifest                                  |
|                                            |                                          |
|                                            v                                          |
|                         [ BACKEND API GATEWAY (Port 8000) ]                           |
|      /api/stt  |  /api/chat  |  /api/tts  |  /api/soil-*  |  /api/mandi  |  /api/weather   |
|                                            |                                          |
|                                            v                                          |
|     +--------------------+   +---------------------+   +--------------------------+   |
|     |  Sarvam AI Cloud   |   |   ICAR Knowledge    |   | Deterministic Guardrails |   |
|     | (Saaras/Bulbul/LLM)|   |  (UASB Agronomy RAG)|   | (CIBRC Banned Intercept) |   |
|     +--------------------+   +---------------------+   +--------------------------+   |
+---------------------------------------------------------------------------------------+
```

---

## 3. Rendering Strategy

### Surface 1: Editorial Landing Site (Static-First)
- **Pre-rendered Static HTML**:
  - Hero narrative, the five agricultural reality challenges, introducing KisanSamvaad, safety and responsible AI policies, Sarvam ecosystem architecture SVG, regional Karnataka impact map, and institutional footer.
  - 100% accessible and readable with JavaScript completely disabled.
- **Dynamic Skeletons**:
  - Live waveform visualizer degrades to a high-contrast SVG waveform poster if Web Audio is unsupported.
  - Interactive Soil Health Card paper preview and diagnostic gauges initialize with authentic default values.

### Surface 2: Farmer-First Application UI (9 Dedicated Screens)
- **Screen 1: Farmer Dashboard**: Daily advisory card, urgent weather spray alerts, mandi ticker, quick voice query launcher.
- **Screen 2: Voice Assistant Room**: Focused audio consultation room with central microphone, code-mixed Indic transcript, and audio controls.
- **Screen 3: Soil Card Scanner**: Drag-and-drop document upload with camera activation, staged OCR progress, and synthetic sample selector.
- **Screen 4: Soil Report Analysis**: Comprehensive N-P-K, pH, and organic carbon diagnostics with manual farmer verification inputs and ICAR remediation steps.
- **Screen 5: Mandi Intelligence**: Filterable commodity prices across Kolar, Yeshwanthpur, Raichur, and Shimoga with modal arbitrage indicators.
- **Screen 6: Weather & Spray Windows**: IMD-calibrated agricultural spray suitability forecasts with wind drift and chemical wash-off warnings.
- **Screen 7: Language Preferences**: Multilingual selector covering Kannada, Hindi, Tamil, Telugu, Marathi, and English with live native script preview.
- **Screen 8: Conversation History**: Chronological log of past voice consultations and soil tests with audio replay and ICAR citations.
- **Screen 9: Help & Expert Assistance**: Direct dialer to nearest Krishi Vigyan Kendra (KVK) extension officer and toll-free 1800 IVR simulator.

---

## 4. Data Provenance Contract

Every dynamic metric or model response implements the strict Data Provenance Contract:

```typescript
type ProvenanceStatus = 'LIVE' | 'CACHED' | 'DEMO' | 'UNAVAILABLE';

interface ProvenanceData<T> {
  status: ProvenanceStatus;
  source: string;
  timestamp: string;
  cache_age_seconds?: number;
  data: T;
  verification_authority?: string; // e.g. "ICAR - UAS Bangalore"
}
```

UI Representation:
- `LIVE`: Green chip (`#052E16` on `#4ADE80`), verified timestamp, source entity.
- `CACHED`: Amber chip (`#451A03` on `#FBBF24`), cache age indicator.
- `DEMO`: Blue chip (`#172554` on `#60A5FA`), synthetic dataset notice.
- `UNAVAILABLE`: Red chip (`#450A0A` on `#F87171`), offline fallback mode.

---

## 5. Security & Key Isolation Architecture

1. **Zero Client Secrets**:
   - The frontend never stores, transmits, or handles raw Sarvam API keys in client-side code.
   - All external API calls terminate at `backend/app/api/routes.py`.
2. **Fail-Safe Demo Mode**:
   - If `SARVAM_API_KEY` is missing or placeholder credentials are detected, the backend and frontend automatically enter `DEMO` mode with realistic scripted responses and clear visual labeling.
3. **Deterministic Safety Guardrails**:
   - All LLM queries and soil remediation suggestions are intercepted outside the stochastic loop by `AgriGuardrails` before reaching the farmer.
   - Queries referencing CIBRC banned pesticides (Endosulfan, Paraquat, Monocrotophos) fail closed immediately with an emergency safety advisory.

