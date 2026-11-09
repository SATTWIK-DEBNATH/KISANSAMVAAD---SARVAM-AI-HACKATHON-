// ============================================================================
// KisanSamvaad Supabase Client Singleton Utility
// File: frontend/lib/supabaseClient.ts
// ============================================================================

import { createClient, SupabaseClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || "";
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";

if (!supabaseUrl || !supabaseAnonKey) {
  if (typeof window !== "undefined") {
    console.warn(
      "[KisanSamvaad] Supabase credentials missing. Ensure NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY are set in .env.local."
    );
  }
}

// Global singleton pattern to prevent duplicate instances during Fast Refresh / HMR
declare global {
  // eslint-disable-next-line no-var
  var __supabaseInstance: SupabaseClient | undefined;
}

export const supabase: SupabaseClient =
  globalThis.__supabaseInstance ??
  createClient(
    supabaseUrl || "https://placeholder-project.supabase.co",
    supabaseAnonKey || "placeholder-anon-key",
    {
      auth: {
        persistSession: true,
        autoRefreshToken: true,
        detectSessionInUrl: true,
        flowType: "pkce",
      },
    }
  );

if (process.env.NODE_ENV !== "production") {
  globalThis.__supabaseInstance = supabase;
}

export default supabase;
