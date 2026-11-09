// ============================================================================
// KisanSamvaad Supabase Authentication Module & Vercel URL Resolver
// File: frontend/lib/supabaseAuth.ts
// ============================================================================

import { supabase } from "./supabaseClient";
import type { Session, User } from "@supabase/supabase-js";

/**
 * Dynamically resolves the authentication redirect URL across local development,
 * dynamic Vercel preview branch deployments, and custom production domains.
 * Ensures wildcard preview environments match Supabase Auth URL allowances.
 */
export function getAuthRedirectURL(path: string = "/"): string {
  let url =
    process.env.NEXT_PUBLIC_SITE_URL ?? // Set this to your custom site URL in production env
    process.env.NEXT_PUBLIC_VERCEL_URL ?? // Automatically provisioned by Vercel on preview deployments
    "http://localhost:8000";

  // Make sure to include https:// when running on Vercel preview deployments
  url = url.startsWith("http") ? url : `https://${url}`;
  // Make sure to remove any trailing slashes before appending path
  url = url.replace(/\/+$/, "");
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${url}${normalizedPath}`;
}

/**
 * Initiate SMS OTP sign-in for Indian farmers using E.164 phone standard (+91XXXXXXXXXX).
 */
export async function sendFarmerPhoneOtp(phoneNumber: string): Promise<{ error: Error | null }> {
  // Format Indian mobile numbers if entered without country code
  let formattedPhone = phoneNumber.trim().replace(/[\s-]/g, "");
  if (!formattedPhone.startsWith("+")) {
    if (formattedPhone.length === 10) {
      formattedPhone = `+91${formattedPhone}`;
    }
  }

  const { error } = await supabase.auth.signInWithOtp({
    phone: formattedPhone,
  });

  return { error };
}

/**
 * Verify 6-digit SMS OTP token submitted by the farmer.
 */
export async function verifyFarmerPhoneOtp(
  phoneNumber: string,
  token: string
): Promise<{ session: Session | null; user: User | null; error: Error | null }> {
  let formattedPhone = phoneNumber.trim().replace(/[\s-]/g, "");
  if (!formattedPhone.startsWith("+")) {
    if (formattedPhone.length === 10) {
      formattedPhone = `+91${formattedPhone}`;
    }
  }

  const { data, error } = await supabase.auth.verifyOtp({
    phone: formattedPhone,
    token: token.trim(),
    type: "sms",
  });

  return { session: data.session, user: data.user, error };
}

/**
 * Passwordless Magic Link email authentication.
 */
export async function sendEmailMagicLink(email: string): Promise<{ error: Error | null }> {
  const redirectUrl = getAuthRedirectURL("/auth/callback");
  const { error } = await supabase.auth.signInWithOtp({
    email: email.trim().toLowerCase(),
    options: {
      emailRedirectTo: redirectUrl,
    },
  });

  return { error };
}

/**
 * Standard Email and Password registration with farmer metadata.
 */
export async function signUpWithEmail(
  email: string,
  password: string,
  metadata: {
    fullName: string;
    phone?: string;
    preferredLanguage?: string;
    district?: string;
    state?: string;
  }
): Promise<{ user: User | null; error: Error | null }> {
  const redirectUrl = getAuthRedirectURL("/auth/callback");
  const { data, error } = await supabase.auth.signUp({
    email: email.trim().toLowerCase(),
    password,
    options: {
      emailRedirectTo: redirectUrl,
      data: {
        full_name: metadata.fullName,
        phone: metadata.phone || "",
        preferred_language: metadata.preferredLanguage || "kn-IN",
        district: metadata.district || "",
        state: metadata.state || "Karnataka",
      },
    },
  });

  return { user: data.user, error };
}

/**
 * Standard Email and Password log-in.
 */
export async function signInWithEmail(
  email: string,
  password: string
): Promise<{ session: Session | null; user: User | null; error: Error | null }> {
  const { data, error } = await supabase.auth.signInWithPassword({
    email: email.trim().toLowerCase(),
    password,
  });

  return { session: data.session, user: data.user, error };
}

/**
 * Google OAuth login initiating PKCE code exchange flow.
 */
export async function signInWithGoogleOAuth(): Promise<{ error: Error | null }> {
  const redirectUrl = getAuthRedirectURL("/auth/callback");
  const { error } = await supabase.auth.signInWithOAuth({
    provider: "google",
    options: {
      redirectTo: redirectUrl,
      queryParams: {
        access_type: "offline",
        prompt: "consent",
      },
    },
  });

  return { error };
}

/**
 * Session termination and cache invalidation.
 */
export async function signOutUser(): Promise<{ error: Error | null }> {
  const { error } = await supabase.auth.signOut();
  return { error };
}

/**
 * Fetch current authenticated user.
 */
export async function getCurrentUser(): Promise<User | null> {
  const { data: { user } } = await supabase.auth.getUser();
  return user;
}
