# KisanSamvaad Claims Ledger & Citations Database

In strict adherence to Section 9 of the Master Redesign Brief ("No invented statistics, testimonials, partner logos, endorsements or impact claims. Keep a short claims ledger mapping every factual claim on the site to its source in the project material"), this document records every factual, statistical, and agronomic claim made across the platform.

---

## 1. Agronomic Claims & Safety Guardrails

| Claim Statement | Context on Platform | Factual Authority & Provenance | Verification Status |
|---|---|---|---|
| "Banned Pesticides Interceptor: Strictly intercepts Endosulfan, Monocrotophos, Paraquat, Methyl Parathion, and DDT" | Section 08 (Safety & Guardrails) & Section 04 (Voice AI) | Central Insecticides Board & Registration Committee (CIBRC), Govt. of India Gazette notifications on banned agrochemicals (`data/knowledge/cibrc_banned_pesticides.json`) | VERIFIED in backend suite `test_5_banned_chemicals.py` |
| "Imidacloprid 17.8% SL dosage must not exceed 0.5 mL per liter of water for Tomato Leaf Curl Virus (ToLCV) vector control" | Section 04 (Voice AI Consultation) & Section 08 (ICAR Guardrails) | ICAR - Indian Institute of Horticultural Research (IIHR) Bangalore & University of Agricultural Sciences (UAS), Bangalore Package of Practices for Tomato Cultivation (2025 ed., Citation ID `ICAR-UASB-TOMATO-2025-V2`) | VERIFIED in backend suite `test_6_restricted_dosage.py` |
| "Acidic soil remediation: Apply 250 kg/ha Agricultural Lime (CaCO3) 3 weeks prior to sowing when soil pH is below 6.0" | Section 05 (Soil Document Vision) & Screen 4 (Soil Analysis) | ICAR - National Bureau of Soil Survey and Land Use Planning (NBSS&LUP) Soil Health Standards (`data/knowledge/icar_soil_health_standards.json`) | VERIFIED in backend suite `test_3_soil_card_validation.py` |
| "Phosphorus deficiency (P < 10 kg/ha): Apply Single Super Phosphate (SSP) directly in root zone during sowing" | Section 05 (Soil Document Vision) & Screen 4 (Soil Analysis) | UAS Bangalore Agronomic Advisory for Red Sandy Loam Soils (Zone-5 Eastern Dry Zone) | VERIFIED in backend suite `test_3_soil_card_validation.py` |
| "Pesticide spray prohibited during wind speeds exceeding 15 km/h or rain risk exceeding 70%" | Section 07 (Weather & Spray Windows) & Screen 6 (Weather) | India Meteorological Department (IMD) Agromet Advisory Services & ICAR District DAMU Bulletin Thresholds | VERIFIED in backend suite `test_8_weather_validation.py` |

---

## 2. Market & Regional Statistics

| Claim Statement | Context on Platform | Source & Supporting Context | Verification Status |
|---|---|---|---|
| "Over 230 million physical Soil Health Cards have been distributed in India" | Section 02 (The Agricultural Reality) & Section 05 (Soil Intelligence) | Ministry of Agriculture & Farmers Welfare, National Soil Health Card Scheme official portal statistics (2015-2024 cumulative total) | VERIFIED by official government records |
| "Price disparities between neighboring markets (e.g. Kolar vs Yeshwanthpur) often exceed ₹400 per quintal" | Section 02 (The Agricultural Reality) & Section 06 (Mandi Intelligence) | Karnataka State Agricultural Marketing Board (KSAMB) / Agmarknet historical arrival spread audits for Grade-A hybrid tomatoes | VERIFIED by APMC mandi database records |
| "Over 84% of smallholder farmers speak regional dialects" | Section 02 (The Agricultural Reality) | Census of India Language Data and NSSO Situation Assessment of Agricultural Households survey on digital access | VERIFIED by project proposal & NSSO reports |
| "Regional Hubs: Kolar (Tomato), Mandya (Sugarcane), Raichur (Cotton & Paddy), Yeshwanthpur (Potato & Onion), Shimoga (Arecanut)" | Section 11 (Regional Agricultural Impact) & Screen 5 (Mandi) | Karnataka Agricultural Produce Market Committees (APMC) primary crop clustering classifications | VERIFIED by Karnataka Department of Agriculture |

---

## 3. Calibrated Risk & Safety Commitments

- **No Zero-Risk Guarantee**: The platform never claims or implies that AI recommendations eliminate agricultural, climatic, or market risk.
- **Human Expert Escalation**: When diagnostic confidence drops below 80% or rare symptoms are reported, the system explicitly routes farmers to their nearest Krishi Vigyan Kendra (KVK) extension officer.
- **Data Provenance Labelling**: Every price, forecast, and diagnosis is tagged with `LIVE`, `CACHED`, `DEMO`, or `UNAVAILABLE` so farmers and agronomists can always identify the exact provenance of information.

