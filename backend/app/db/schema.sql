-- KisanSamvaad SQLite Relational Persistence Schema
-- Optimized for low-resource environments (<100MB RAM) with WAL mode

CREATE TABLE IF NOT EXISTS farmers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    village TEXT,
    district TEXT,
    state TEXT DEFAULT 'Karnataka',
    preferred_language TEXT DEFAULT 'kn-IN',
    landholding_acres REAL DEFAULT 1.0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS farms (
    id TEXT PRIMARY KEY,
    farmer_id TEXT NOT NULL,
    plot_name TEXT,
    survey_number TEXT,
    area_acres REAL DEFAULT 1.0,
    soil_type TEXT DEFAULT 'Red Sandy Loam',
    irrigation_source TEXT DEFAULT 'Borewell',
    created_at TEXT NOT NULL,
    FOREIGN KEY (farmer_id) REFERENCES farmers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crops (
    id TEXT PRIMARY KEY,
    farm_id TEXT NOT NULL,
    crop_name TEXT NOT NULL,
    variety TEXT,
    sowing_date TEXT,
    stage TEXT DEFAULT 'Vegetative',
    expected_harvest_date TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (farm_id) REFERENCES farms(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS soil_reports (
    id TEXT PRIMARY KEY,
    farm_id TEXT,
    card_number TEXT,
    nitrogen REAL NOT NULL,
    phosphorus REAL NOT NULL,
    potassium REAL NOT NULL,
    ph REAL NOT NULL,
    organic_carbon REAL NOT NULL,
    zinc REAL NOT NULL,
    boron REAL NOT NULL,
    test_date TEXT NOT NULL,
    recommendations_json TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (farm_id) REFERENCES farms(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    farmer_id TEXT,
    query_text TEXT NOT NULL,
    response_text TEXT NOT NULL,
    language TEXT DEFAULT 'kn-IN',
    detected_intent TEXT,
    audio_duration REAL DEFAULT 0.0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (farmer_id) REFERENCES farmers(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS market_observations (
    id TEXT PRIMARY KEY,
    market_name TEXT NOT NULL,
    district TEXT,
    commodity TEXT NOT NULL,
    variety TEXT,
    min_price REAL NOT NULL,
    max_price REAL NOT NULL,
    modal_price REAL NOT NULL,
    date TEXT NOT NULL,
    data_source_mode TEXT DEFAULT 'DEMO',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS schemes (
    id TEXT PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    name_en TEXT NOT NULL,
    name_hi TEXT NOT NULL,
    name_kn TEXT NOT NULL,
    category TEXT NOT NULL,
    benefit_summary TEXT NOT NULL,
    eligibility_criteria_json TEXT,
    portal_url TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS expert_cases (
    id TEXT PRIMARY KEY,
    farmer_id TEXT,
    query_id TEXT,
    crop_name TEXT NOT NULL,
    symptom_summary TEXT NOT NULL,
    initial_diagnosis TEXT NOT NULL,
    confidence_score REAL NOT NULL,
    escalation_status TEXT DEFAULT 'OPEN',
    assigned_kvk TEXT DEFAULT 'KVK Kolar, ICAR',
    created_at TEXT NOT NULL,
    FOREIGN KEY (farmer_id) REFERENCES farmers(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_farmers_phone ON farmers(phone);
CREATE INDEX IF NOT EXISTS idx_farms_farmer_id ON farms(farmer_id);
CREATE INDEX IF NOT EXISTS idx_crops_farm_id ON crops(farm_id);
CREATE INDEX IF NOT EXISTS idx_conversations_farmer_id ON conversations(farmer_id);
CREATE INDEX IF NOT EXISTS idx_market_commodity ON market_observations(commodity, market_name);

