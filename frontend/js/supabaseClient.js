// ============================================================================
// KisanSamvaad: Supabase Client Singleton Utility (ES Module)
// File: frontend/js/supabaseClient.js
// ============================================================================

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

export const SUPABASE_URL = "https://gqpwfenjodqhtweheqvb.supabase.co";
export const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_1DHgED4hyE_qYM_8dD0q7Q_zUADAprp";

export const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
    flowType: "pkce"
  }
});

/**
 * Initiates Supabase Google OAuth authentication.
 * Automatically redirects back to /login with session tokens, then forwards to /app.
 */
export async function signInWithGoogle(redirectToPath = "/app") {
  const currentOrigin = window.location.origin;
  const callbackUrl = `${currentOrigin}/login?redirect=${encodeURIComponent(redirectToPath)}`;

  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: "google",
    options: {
      redirectTo: callbackUrl,
      queryParams: {
        access_type: "offline",
        prompt: "consent"
      }
    }
  });

  if (error) {
    console.error("Supabase Google OAuth error:", error.message);
    throw error;
  }
  return data;
}

/**
 * Ends the active Supabase session and clears local farmer profile cache.
 */
export async function signOutUser() {
  try {
    await supabase.auth.signOut();
  } catch (err) {
    console.warn("Sign out warning:", err);
  } finally {
    localStorage.removeItem("kisansamvaad_demo_user");
    localStorage.removeItem("kisansamvaad_cached_profile");
    sessionStorage.clear();
    window.location.replace("/");
  }
}
