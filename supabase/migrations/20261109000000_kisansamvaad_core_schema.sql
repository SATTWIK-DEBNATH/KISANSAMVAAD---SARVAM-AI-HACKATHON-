-- ============================================================================
-- KisanSamvaad Production PostgreSQL Schema & Supabase Architecture Migration
-- Version: 20261109000000_kisansamvaad_core_schema.sql
-- Description: Core relational schema, automated profile provisioning trigger,
--              strict Row Level Security (RLS) policies, and Object Storage
--              bucket security configuration for KisanSamvaad AgriTech BaaS.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. PostgreSQL Extensions Setup
-- ----------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ----------------------------------------------------------------------------
-- 2. Utility Trigger: Automated updated_at Timestamp Synchronization
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    NEW.updated_at = timezone('utc'::text, now());
    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION public.handle_updated_at() IS 
'Enforces atomic UTC timestamp synchronization across mutable entities.';

-- ----------------------------------------------------------------------------
-- 3. Core Entity: public.profiles (Linked 1:1 with auth.users)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    phone TEXT,
    full_name TEXT NOT NULL DEFAULT '',
    village TEXT,
    district TEXT NOT NULL DEFAULT '',
    state TEXT NOT NULL DEFAULT 'Karnataka',
    preferred_language TEXT NOT NULL DEFAULT 'kn-IN',
    landholding_acres NUMERIC(6, 2) NOT NULL DEFAULT 1.00,
    agristack_fid TEXT,
    avatar_url TEXT,
    is_onboarded BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

COMMENT ON TABLE public.profiles IS 
'Stores public business and agricultural attributes for authenticated farmers. Id directly mirrors auth.users.id.';

CREATE TRIGGER set_profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- ----------------------------------------------------------------------------
-- 4. Automated User Profile Provisioning Trigger
-- ----------------------------------------------------------------------------
-- SECURITY DEFINER ensures execution runs with table owner permissions rather
-- than the unprivileged caller context, while SET search_path protects against
-- schema-spoofing injection attacks.
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    INSERT INTO public.profiles (
        id,
        phone,
        full_name,
        preferred_language,
        created_at,
        updated_at
    )
    VALUES (
        NEW.id,
        COALESCE(NEW.phone, NEW.raw_user_meta_data->>'phone', ''),
        COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.raw_user_meta_data->>'name', ''),
        COALESCE(NEW.raw_user_meta_data->>'preferred_language', 'kn-IN'),
        timezone('utc'::text, now()),
        timezone('utc'::text, now())
    )
    ON CONFLICT (id) DO NOTHING;
    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION public.handle_new_user() IS 
'Automates zero-latency profile row instantiation whenever an identity registers in auth.users.';

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ----------------------------------------------------------------------------
-- 5. Core Entity: public.farms (Agricultural Landholdings)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.farms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    plot_name TEXT NOT NULL DEFAULT 'Main Plot',
    survey_number TEXT,
    area_acres NUMERIC(6, 2) NOT NULL DEFAULT 1.00,
    soil_type TEXT NOT NULL DEFAULT 'Red Sandy Loam',
    irrigation_source TEXT NOT NULL DEFAULT 'Borewell',
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

CREATE TRIGGER set_farms_updated_at
    BEFORE UPDATE ON public.farms
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- ----------------------------------------------------------------------------
-- 6. Core Entity: public.crops (Active Plantings & Seasonal Rotations)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.crops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farm_id UUID NOT NULL REFERENCES public.farms(id) ON DELETE CASCADE,
    crop_name TEXT NOT NULL,
    variety TEXT,
    sowing_date DATE,
    stage TEXT NOT NULL DEFAULT 'Vegetative',
    expected_harvest_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

CREATE TRIGGER set_crops_updated_at
    BEFORE UPDATE ON public.crops
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- ----------------------------------------------------------------------------
-- 7. Core Entity: public.soil_reports (Soil Health Cards & Micro-nutrients)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.soil_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    farm_id UUID REFERENCES public.farms(id) ON DELETE SET NULL,
    card_number TEXT,
    storage_file_path TEXT,
    nitrogen_kg_ha NUMERIC(7, 2) NOT NULL DEFAULT 0.00,
    phosphorus_kg_ha NUMERIC(7, 2) NOT NULL DEFAULT 0.00,
    potassium_kg_ha NUMERIC(7, 2) NOT NULL DEFAULT 0.00,
    ph_level NUMERIC(4, 2) NOT NULL DEFAULT 7.00,
    organic_carbon_percent NUMERIC(4, 2) NOT NULL DEFAULT 0.50,
    zinc_ppm NUMERIC(6, 2) NOT NULL DEFAULT 0.60,
    boron_ppm NUMERIC(6, 2) NOT NULL DEFAULT 0.50,
    test_date DATE NOT NULL DEFAULT CURRENT_DATE,
    recommendations_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

CREATE TRIGGER set_soil_reports_updated_at
    BEFORE UPDATE ON public.soil_reports
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- ----------------------------------------------------------------------------
-- 8. Core Entity: public.fertilizer_plans (Whole-Bag Nutrition Schedules)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.fertilizer_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    farm_id UUID REFERENCES public.farms(id) ON DELETE SET NULL,
    soil_report_id UUID REFERENCES public.soil_reports(id) ON DELETE SET NULL,
    crop_name TEXT NOT NULL,
    target_acreage NUMERIC(6, 2) NOT NULL DEFAULT 1.00,
    urea_50kg_bags INTEGER NOT NULL DEFAULT 0,
    dap_50kg_bags INTEGER NOT NULL DEFAULT 0,
    mop_50kg_bags INTEGER NOT NULL DEFAULT 0,
    ssp_50kg_bags INTEGER NOT NULL DEFAULT 0,
    total_estimated_cost_inr NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    weather_risk_flag BOOLEAN NOT NULL DEFAULT FALSE,
    imd_forecast_summary TEXT,
    schedule_milestones_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ----------------------------------------------------------------------------
-- 9. Core Entity: public.conversations (Conversational Voice Sessions)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL DEFAULT 'New Voice Consultation',
    language_code TEXT NOT NULL DEFAULT 'kn-IN',
    last_intent TEXT,
    is_pinned BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

CREATE TRIGGER set_conversations_updated_at
    BEFORE UPDATE ON public.conversations
    FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- ----------------------------------------------------------------------------
-- 10. Core Entity: public.chat_messages (Multilingual Utterances & Audio)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES public.conversations(id) ON DELETE CASCADE,
    sender_role TEXT NOT NULL CHECK (sender_role IN ('user', 'assistant', 'system')),
    content_text TEXT NOT NULL,
    audio_input_storage_path TEXT,
    audio_output_url TEXT,
    asr_confidence NUMERIC(4, 3),
    latency_ms INTEGER,
    tokens_used INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ----------------------------------------------------------------------------
-- 11. Core Entity: public.saved_advice (Bookmarked Crop Knowledge)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.saved_advice (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    conversation_id UUID REFERENCES public.conversations(id) ON DELETE SET NULL,
    category TEXT NOT NULL DEFAULT 'CROP_CARE',
    headline TEXT NOT NULL,
    body_markdown TEXT NOT NULL,
    tags TEXT[] NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ----------------------------------------------------------------------------
-- 12. Performance B-Tree Indexes
-- ----------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_profiles_phone ON public.profiles(phone);
CREATE INDEX IF NOT EXISTS idx_profiles_district ON public.profiles(district, state);
CREATE INDEX IF NOT EXISTS idx_farms_farmer_id ON public.farms(farmer_id);
CREATE INDEX IF NOT EXISTS idx_crops_farm_id ON public.crops(farm_id);
CREATE INDEX IF NOT EXISTS idx_soil_reports_farmer_id ON public.soil_reports(farmer_id);
CREATE INDEX IF NOT EXISTS idx_fertilizer_plans_farmer_id ON public.fertilizer_plans(farmer_id);
CREATE INDEX IF NOT EXISTS idx_conversations_farmer_id ON public.conversations(farmer_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_conv_id ON public.chat_messages(conversation_id, created_at ASC);
CREATE INDEX IF NOT EXISTS idx_saved_advice_farmer_id ON public.saved_advice(farmer_id);

-- ----------------------------------------------------------------------------
-- 13. Security Hardening: Row Level Security (Default Deny Posture)
-- ----------------------------------------------------------------------------
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.farms ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.crops ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.soil_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fertilizer_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.saved_advice ENABLE ROW LEVEL SECURITY;

ALTER TABLE public.profiles FORCE ROW LEVEL SECURITY;
ALTER TABLE public.farms FORCE ROW LEVEL SECURITY;
ALTER TABLE public.crops FORCE ROW LEVEL SECURITY;
ALTER TABLE public.soil_reports FORCE ROW LEVEL SECURITY;
ALTER TABLE public.fertilizer_plans FORCE ROW LEVEL SECURITY;
ALTER TABLE public.conversations FORCE ROW LEVEL SECURITY;
ALTER TABLE public.chat_messages FORCE ROW LEVEL SECURITY;
ALTER TABLE public.saved_advice FORCE ROW LEVEL SECURITY;

-- ----------------------------------------------------------------------------
-- 14. Granular RLS Policies (USING vs WITH CHECK)
-- ----------------------------------------------------------------------------

-- PROFILES POLICIES
-- USING clause inspects the row before returning or reading.
-- WITH CHECK clause prevents spoofing the foreign key to an identity other than auth.uid().
CREATE POLICY "profiles_owner_select" ON public.profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "profiles_owner_update" ON public.profiles
    FOR UPDATE USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

CREATE POLICY "profiles_owner_insert" ON public.profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

-- FARMS POLICIES
CREATE POLICY "farms_owner_select" ON public.farms
    FOR SELECT USING (auth.uid() = farmer_id);

CREATE POLICY "farms_owner_insert" ON public.farms
    FOR INSERT WITH CHECK (auth.uid() = farmer_id);

CREATE POLICY "farms_owner_update" ON public.farms
    FOR UPDATE USING (auth.uid() = farmer_id)
    WITH CHECK (auth.uid() = farmer_id);

CREATE POLICY "farms_owner_delete" ON public.farms
    FOR DELETE USING (auth.uid() = farmer_id);

-- CROPS POLICIES (Nested ownership check via farms relation)
CREATE POLICY "crops_owner_select" ON public.crops
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.farms f
            WHERE f.id = crops.farm_id AND f.farmer_id = auth.uid()
        )
    );

CREATE POLICY "crops_owner_insert" ON public.crops
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.farms f
            WHERE f.id = crops.farm_id AND f.farmer_id = auth.uid()
        )
    );

CREATE POLICY "crops_owner_update" ON public.crops
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.farms f
            WHERE f.id = crops.farm_id AND f.farmer_id = auth.uid()
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.farms f
            WHERE f.id = crops.farm_id AND f.farmer_id = auth.uid()
        )
    );

CREATE POLICY "crops_owner_delete" ON public.crops
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM public.farms f
            WHERE f.id = crops.farm_id AND f.farmer_id = auth.uid()
        )
    );

-- SOIL REPORTS POLICIES
CREATE POLICY "soil_reports_owner_select" ON public.soil_reports
    FOR SELECT USING (auth.uid() = farmer_id);

CREATE POLICY "soil_reports_owner_insert" ON public.soil_reports
    FOR INSERT WITH CHECK (auth.uid() = farmer_id);

CREATE POLICY "soil_reports_owner_update" ON public.soil_reports
    FOR UPDATE USING (auth.uid() = farmer_id)
    WITH CHECK (auth.uid() = farmer_id);

CREATE POLICY "soil_reports_owner_delete" ON public.soil_reports
    FOR DELETE USING (auth.uid() = farmer_id);

-- FERTILIZER PLANS POLICIES
CREATE POLICY "fertilizer_plans_owner_select" ON public.fertilizer_plans
    FOR SELECT USING (auth.uid() = farmer_id);

CREATE POLICY "fertilizer_plans_owner_insert" ON public.fertilizer_plans
    FOR INSERT WITH CHECK (auth.uid() = farmer_id);

CREATE POLICY "fertilizer_plans_owner_delete" ON public.fertilizer_plans
    FOR DELETE USING (auth.uid() = farmer_id);

-- CONVERSATIONS POLICIES
CREATE POLICY "conversations_owner_select" ON public.conversations
    FOR SELECT USING (auth.uid() = farmer_id);

CREATE POLICY "conversations_owner_insert" ON public.conversations
    FOR INSERT WITH CHECK (auth.uid() = farmer_id);

CREATE POLICY "conversations_owner_update" ON public.conversations
    FOR UPDATE USING (auth.uid() = farmer_id)
    WITH CHECK (auth.uid() = farmer_id);

CREATE POLICY "conversations_owner_delete" ON public.conversations
    FOR DELETE USING (auth.uid() = farmer_id);

-- CHAT MESSAGES POLICIES (Nested ownership check via conversations)
CREATE POLICY "messages_owner_select" ON public.chat_messages
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.conversations c
            WHERE c.id = chat_messages.conversation_id AND c.farmer_id = auth.uid()
        )
    );

CREATE POLICY "messages_owner_insert" ON public.chat_messages
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.conversations c
            WHERE c.id = chat_messages.conversation_id AND c.farmer_id = auth.uid()
        )
    );

CREATE POLICY "messages_owner_delete" ON public.chat_messages
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM public.conversations c
            WHERE c.id = chat_messages.conversation_id AND c.farmer_id = auth.uid()
        )
    );

-- SAVED ADVICE POLICIES
CREATE POLICY "saved_advice_owner_select" ON public.saved_advice
    FOR SELECT USING (auth.uid() = farmer_id);

CREATE POLICY "saved_advice_owner_insert" ON public.saved_advice
    FOR INSERT WITH CHECK (auth.uid() = farmer_id);

CREATE POLICY "saved_advice_owner_delete" ON public.saved_advice
    FOR DELETE USING (auth.uid() = farmer_id);

-- ----------------------------------------------------------------------------
-- 15. Object Storage Configuration: Buckets & Path-Based Isolation
-- ----------------------------------------------------------------------------
-- Create dedicated private buckets for farmer media and soil health cards.
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES
    ('soil-cards', 'soil-cards', FALSE, 10485760, ARRAY['image/jpeg', 'image/png', 'image/webp', 'application/pdf']),
    ('farmer-media', 'farmer-media', FALSE, 26214400, ARRAY['audio/wav', 'audio/mp3', 'audio/webm', 'audio/ogg', 'image/jpeg', 'image/png'])
ON CONFLICT (id) DO UPDATE SET
    public = EXCLUDED.public,
    file_size_limit = EXCLUDED.file_size_limit,
    allowed_mime_types = EXCLUDED.allowed_mime_types;

-- Storage RLS: Ensure each farmer can strictly interact only with objects
-- whose top-level folder matches their authenticated UUID string:
-- Object path structure: `<auth.uid()>/<file-uuid>.<extension>`
CREATE POLICY "farmer_read_own_media" ON storage.objects
    FOR SELECT TO authenticated
    USING (
        bucket_id IN ('soil-cards', 'farmer-media')
        AND (storage.foldername(name))[1] = auth.uid()::text
    );

CREATE POLICY "farmer_upload_own_media" ON storage.objects
    FOR INSERT TO authenticated
    WITH CHECK (
        bucket_id IN ('soil-cards', 'farmer-media')
        AND (storage.foldername(name))[1] = auth.uid()::text
    );

CREATE POLICY "farmer_update_own_media" ON storage.objects
    FOR UPDATE TO authenticated
    USING (
        bucket_id IN ('soil-cards', 'farmer-media')
        AND (storage.foldername(name))[1] = auth.uid()::text
    )
    WITH CHECK (
        bucket_id IN ('soil-cards', 'farmer-media')
        AND (storage.foldername(name))[1] = auth.uid()::text
    );

CREATE POLICY "farmer_delete_own_media" ON storage.objects
    FOR DELETE TO authenticated
    USING (
        bucket_id IN ('soil-cards', 'farmer-media')
        AND (storage.foldername(name))[1] = auth.uid()::text
    );
