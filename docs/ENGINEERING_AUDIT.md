# KisanSamvaad - Comprehensive Engineering Audit
## Sovereign Indic Voice and Document AI for Indian Agriculture

Date: November 2026  
Status: Phase 0 Engineering Baseline Assessment  
Auditor: Principal Systems Architect & Engineering Lead  
Target Constraints: Low-Resource (<100MB RAM), Dual Execution Mode (Simulated / Live Sarvam AI), Zero Tolerance for Unsafe Agrochemical Hallucinations  

---

## 1. Executive Summary & Purpose

KisanSamvaad (Kisan Samvaad / Kisan Sanvaada) is designed to bridge the digital literacy, linguistic diversity, and information access divide confronting Indian farmers. The platform delivers voice-first agricultural advisory, Soil Health Card parsing, APMC Mandi market intelligence, and weather-driven spray window alerts grounded in Indian Council of Agricultural Research (ICAR) packages of practices and Central Insecticide Board and Registration Committee (CIBRC) safety regulations.

This engineering audit examines the entire existing codebase, cataloging verified functional subsystems, partially implemented interfaces, simulated components, broken/missing modules, security boundaries, and architectural technical debt.

---

## 2. Existing Architecture Analysis

The existing system follows a modular, lightweight Python service-oriented design built on top of standard Python libraries (`http.server`, `urllib.request`, `dataclasses`, `sqlite3` capable). This design intentionally avoids heavy runtime frameworks to satisfy the primary hardware constraint: execution on low-cost rural extension center hardware (e.g., 4GB to 8GB RAM mini PCs, KVK desktops) with an active operational memory footprint under 100MB.

### Architectural Tiers:
1. Client Access Tier:
   - Voice-first progressive web interface (PWA) supporting touch-free voice interaction and physical Soil Health Card camera uploads.
   - 1800-series PSTN Toll-Free IVR telephony integration interface for feature phone access.
2. Ingress & Routing Tier (`backend/server.py` & `backend/app/api/routes.py`):
   - Threaded HTTP server (`ThreadingMixIn`) with CORS headers, JSON request decoding, and query parsing.
   - Route dispatcher separating GET discovery/query routes from POST computational/AI pipelines.
3. Sovereign AI Integration Tier (`backend/app/integrations/sarvam/`):
   - Unified Sarvam client wrapping Saaras ASR (speech-to-text), Bulbul TTS (text-to-speech), Sarvam-1 LLM (Indic reasoning), Document Vision (soil card OCR), and Mayura (translation).
4. Safety & Grounding Tier (`backend/app/safety/` & `backend/app/ai/rag/`):
   - Deterministic AgriGuardrail engine acting as a fail-closed interceptor for banned agrochemicals (Endosulfan, Monocrotophos, Paraquat) and dosage caps (Imidacloprid <= 0.5 ml/L).
   - ICAR UAS-Bangalore and CICR agronomic knowledge base with structured provenance metadata.
5. Agricultural Services Tier (`backend/app/services/`):
   - Soil diagnostic service mapping 7 core parameters (N, P, K, pH, OC, Zinc, Boron) to ICAR deficiency thresholds.
   - Telephony IVR state machine mapping DTMF key presses (1-4) to voice prompts in Kannada and Hindi.
   - APMC Mandi connector tracking commodity modal rates with freshness timestamps.
   - Weather connector providing spray-window safety evaluations based on wind and precipitation risk.

---

## 3. Current Implementation Status Breakdown

The codebase currently stands at high unit test maturity for core algorithms (10 suites, 31 verification tests passing 100% in 0.07s). However, several modules remain stateless or rely on in-memory representations rather than persistent relational storage.

### Subsystem Status Matrix:

| Subsystem / Module | Implementation Status | Grounding / Provider | Verified In Test Suite |
| :--- | :--- | :--- | :--- |
| Core HTTP Dispatcher | Functional | Python standard library | Yes (Suites 9, 10) |
| Sarvam Saaras ASR Adapter | Functional (Dual-Mode) | Live Sarvam API / Calibrated Fallback | Yes (Suite 1, 2) |
| Sarvam Bulbul TTS Adapter | Functional (Dual-Mode) | Live Sarvam API / Calibrated WAV Synth | Yes (Suite 2) |
| Sarvam-1 Indic LLM Adapter | Functional (Dual-Mode) | Live Sarvam API / ICAR RAG Fallback | Yes (Suite 4) |
| Document Vision Soil OCR | Functional (Dual-Mode) | Live Sarvam API / Calibrated Demo Parser | Yes (Suite 3) |
| Mayura Translation Adapter | Functional (Dual-Mode) | Live Sarvam API / Calibrated Dictionary | Yes (Suite 10) |
| AgriGuardrails (Banned Chem) | Functional (Strict) | CIBRC Gazette / Deterministic Regex | Yes (Suite 5) |
| AgriGuardrails (Dosage Bounds)| Functional (Strict) | ICAR UAS-B / Quantitative Bounds | Yes (Suite 6) |
| Soil Diagnostic Evaluation | Functional | ICAR UAS-B Soil Standards | Yes (Suite 3) |
| APMC Mandi Rates Connector | Functional (Simulated) | Real Market Benchmarks (Kolar/Raichur) | Yes (Suite 7) |
| IMD Weather Advisory | Functional (Simulated) | IMD Spray Thresholds | Yes (Suite 8) |
| Telephony IVR Flow | Partially Implemented | DTMF State Handler | Yes (Suite 10) |
| Relational Persistence | Missing (In-Memory) | Volatile Process Memory | Partial |
| Net Realisation Calculator | Missing | N/A | No |
| Multimodal Crop Diagnostics | Missing | N/A | No |
| Comprehensive Schemes Engine| Partially Implemented | Static List in routes.py | No |
| Containerization (Docker) | Missing | None | No |

---

## 4. Functional Components (Verified)

The following components are fully implemented, verified, and passing all automated test suites:

1. Deterministic AgriGuardrail Engine (`backend/app/safety/agri_guardrails.py`):
   - Intercepts all queries and generated text before farmer display.
   - Detects banned substances (Endosulfan, Paraquat, Monocrotophos, DDT, Aldrin, Methyl Parathion).
   - Validates dosage concentrations (e.g., Imidacloprid capped at 0.5 ml/L, Chlorpyrifos capped at 2.5 ml/L, foliar Urea capped at 2.0%).
   - Generates multilingual warning notices in Kannada, Hindi, and English.
   - Maintains an in-memory audit trail of safety violations.

2. ICAR-Grounded RAG Pipeline (`backend/app/ai/rag/`):
   - Stores UAS Bangalore package of practices for Tomato (ICAR-UASB-TOMATO-2025-V2) and CICR Cotton (ICAR-CICR-COTTON-2024-V3).
   - Emits structured provenance citations with document IDs, source institutions, and version numbers.

3. Soil Diagnostic Service (`backend/app/services/soil_service.py`):
   - Evaluates Nitrogen, Phosphorus, Potassium, pH, Organic Carbon, Zinc, and Boron.
   - Calculates custom remediation actions:
     - Acidic soil (pH < 6.5) -> Agricultural Lime (250 kg/ha).
     - Alkaline soil (pH > 8.0) -> Gypsum (500 kg/ha) plus green manure.
     - Low Nitrogen -> Split Urea and Farm Yard Manure (FYM).
   - Delivers multilingual recommendations in Kannada, Hindi, and English.

4. Dual-Mode Sarvam AI Client SDK (`backend/app/integrations/sarvam/`):
   - Automatic key validation preventing crashes when credentials are unset or placeholder strings.
   - Clean failover to calibrated local agronomic simulation models when running offline or without credentials.
   - Transparent reporting of data provider status in response payloads.

---

## 5. Partially Implemented Components

1. Telephony IVR Gateway (`backend/app/services/telephony_service.py`):
   - Current status: DTMF routing logic maps keys '1' (Soil), '2' (Mandi), '3' (Weather), and '4' (Pest).
   - Gap: Audio payload generation returns mock WAV audio identifiers without connecting to a live PSTN SIP trunk or Twilio/Exotel webhook handler.
2. Soil Health Card OCR Parser (`backend/app/integrations/sarvam/vision.py`):
   - Current status: Calibrated simulation parser parses known sample cards accurately with parameter confidence ratings; live route invokes Sarvam Document Vision API when keys exist.
   - Gap: Multipart form-data parser in the standard library HTTP server does not extract arbitrary raw camera image bytes from binary multi-part uploads without manual byte boundary parsing.
3. Government Schemes Service (`backend/app/api/routes.py`):
   - Current status: Returns a static list of 4 schemes (PM-KISAN, PMFBY, Soil Health Card Scheme, PM-KUSUM).
   - Gap: Lacks personalized eligibility assessment, state-specific schemes (such as Karnataka Raita Siri), landholding filtering, and documentation checklist guidance.

---

## 6. Mocked Components

1. APMC Mandi Market Prices (`backend/app/integrations/mandi/connector.py`):
   - Currently returns calibrated real market rates for Karnataka and National trade hubs (Kolar Tomato ₹1,850/qtl, Raichur Cotton ₹7,200/qtl, Lasalgaon Onion ₹2,400/qtl).
   - All records are explicitly labeled with `data_source_mode: "DEMO"` and include fresh timestamps.
   - Live integration with data.gov.in Agmarknet API requires external API credentials and network access.
2. IMD Weather Forecasting (`backend/app/integrations/weather/connector.py`):
   - Currently generates calibrated 3-day forecasts based on Kolar and Raichur climatological patterns.
   - Evaluates wind speed against the 15 km/h spray threshold and rain chance against 60% wash-off threshold.
   - Operates in simulated mode when external weather services are offline.

---

## 7. Broken or Missing Functionality

1. Relational Persistence Layer:
   - Missing: No persistent storage for Farmer Profiles, Farm Plots, Soil History, Consultation Logs, or Market Observations.
   - Consequence: Restarting the server clears all state. Consultation history and farmer context cannot be retained across sessions.
2. Net Realisation Calculator:
   - Missing: Farmers currently see raw mandi modal rates but cannot calculate their net profit after factoring in transport costs, labor loading fees, mandi commission (APMC market fee), bag packaging costs, and transit spoilage.
   - Requirement: A deterministic calculator comparing local mandi (e.g. Kolar) against terminal mandi (e.g. Yeshwanthpur/Bengaluru) to help farmers decide where to sell.
3. Multimodal Crop Diagnostics:
   - Missing: Dedicated crop disease and pest identification pipeline with explicit experimental labeling, confidence score bounds, differential diagnosis, and escalation to KVK human experts.
4. Containerization & Production Infrastructure:
   - Missing: No `Dockerfile`, `docker-compose.yml`, or `.env.example`.
   - Consequence: Deployment requires manual environment variable export and local Python setup.

---

## 8. Security & Safety Concerns

1. Agrochemical Toxicity Hallucinations:
   - Severity: Critical. Recommending banned chemicals or incorrect dosages can cause crop destruction, toxic residue, or human poisoning.
   - Current Mitigation: Deterministic regex and numerical bounds interceptor (`AgriGuardrailEngine`).
   - Audit Finding: Current regex catches primary banned names (Endosulfan, Paraquat, Monocrotophos) but needs expanded coverage for regional trade names (e.g., Thiodan, Gramoxone, Nuvacron).
2. Secret Management:
   - Current Mitigation: `settings.sarvam_api_key` reads from `SARVAM_API_KEY` environment variable.
   - Audit Finding: No hardcoded API keys detected in repository source code. However, `.env.example` is missing to guide developers on safe configuration.
3. Audio Payload Ingestion:
   - Severity: Medium. Unsanitized base64 audio strings could lead to memory exhaustion (Denial of Service) if arbitrarily large payloads are accepted.
   - Audit Finding: Need payload size limits (e.g., 5MB cap) on incoming audio base64 streams.
4. Fail-Closed Design:
   - Verified: When safety checks fail, the system returns a safe warning notice and does not execute or display the unverified response.

---

## 9. Technical Debt Assessment

1. Process-Bound Web Server:
   - Python's `http.server` handles incoming requests synchronously per thread. While sufficient for lightweight extension center setups, it lacks async I/O and formal OpenAPI automatic documentation.
   - Solution: Retain the ultra-lightweight zero-dependency server as the default runtime, but provide structured typed endpoints and an optional ASGI/FastAPI adapter for enterprise deployments.
2. Lack of Centralized Persistence:
   - Data entities are represented only as transient dataclasses in memory.
   - Solution: Implement a lightweight SQLite-backed persistence repository with thread-safe connection pooling that runs without external database processes.

---

## 10. Recommended Improvements & Next Steps

1. Milestone 1: Relational Persistence Layer
   - Create SQLite-backed repository (`backend/app/db/`) supporting Farmer, Farm, Crop, SoilReport, Conversation, and MarketObservation entities.
2. Milestone 2: Net Realisation Economic Calculator
   - Implement deterministic financial calculation module (`backend/app/services/calculator_service.py`) comparing local vs terminal mandis.
3. Milestone 3: Multimodal Crop Diagnostics Subsystem
   - Implement `/api/crop-diagnostics` with differential diagnosis, experimental confidence scores, and KVK escalation triggers.
4. Milestone 4: Enhanced Government Schemes Engine
   - Implement `/api/schemes/evaluate` for personalized eligibility and document verification checklists.
5. Milestone 5: Infrastructure & Containerization
   - Create `Dockerfile`, `docker-compose.yml`, and `.env.example`.
6. Milestone 6: Complete Engineering Documentation Suite
   - Author `docs/IMPLEMENTATION_ROADMAP.md`, `docs/ARCHITECTURE.md`, `docs/API_DOCUMENTATION.md`, `docs/INTEGRATION_STATUS.md`, `docs/SECURITY.md`, `docs/TESTING.md`, and `docs/DEPLOYMENT.md`.
7. Milestone 7: Test Suite Expansion & Validation
   - Add automated test suites for all new modules and verify 100% test pass rate.

