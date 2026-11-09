// ============================================================================
// KisanSamvaad Direct Object Storage Upload Client
// File: frontend/lib/storageUpload.ts
// ============================================================================

import { supabase } from "./supabaseClient";

export interface UploadResult {
  path: string | null;
  publicUrl: string | null;
  signedUrl: string | null;
  error: Error | null;
}

/**
 * Generates a clean random UUID for filename isolation.
 */
function generateUuid(): string {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

/**
 * Uploads a Soil Health Card photo or PDF directly to the 'soil-cards' bucket.
 * Enforces the strict storage RLS policy: (storage.foldername(name))[1] = auth.uid()::text
 */
export async function uploadSoilHealthCard(
  file: File | Blob,
  fileExtension: string = "jpg"
): Promise<UploadResult> {
  const { data: { user }, error: authError } = await supabase.auth.getUser();

  if (authError || !user) {
    return {
      path: null,
      publicUrl: null,
      signedUrl: null,
      error: new Error("Authentication required: Only authenticated farmers can upload soil cards."),
    };
  }

  // Construct isolated storage path conforming strictly to RLS policies
  const fileId = generateUuid();
  const cleanExt = fileExtension.replace(/^\./, "");
  const storagePath = `${user.id}/${fileId}.${cleanExt}`;

  // Direct upload to Supabase Storage bypasses middle-tier application servers
  const { data, error } = await supabase.storage
    .from("soil-cards")
    .upload(storagePath, file, {
      cacheControl: "3600",
      upsert: false,
      contentType: file.type || "application/octet-stream",
    });

  if (error) {
    return { path: null, publicUrl: null, signedUrl: null, error };
  }

  // Generate a temporary 60-minute signed URL for authenticated reading
  const { data: signedData } = await supabase.storage
    .from("soil-cards")
    .createSignedUrl(storagePath, 3600);

  return {
    path: data.path,
    publicUrl: null, // Soil cards are private and protected by RLS
    signedUrl: signedData?.signedUrl ?? null,
    error: null,
  };
}

/**
 * Uploads farmer microphone voice recordings directly to 'farmer-media' bucket.
 */
export async function uploadFarmerVoiceAudio(
  audioBlob: Blob,
  format: "webm" | "wav" | "ogg" = "webm"
): Promise<UploadResult> {
  const { data: { user }, error: authError } = await supabase.auth.getUser();

  if (authError || !user) {
    return {
      path: null,
      publicUrl: null,
      signedUrl: null,
      error: new Error("Authentication required: Only authenticated farmers can upload voice audio."),
    };
  }

  const fileId = generateUuid();
  const storagePath = `${user.id}/${fileId}.${format}`;

  const { data, error } = await supabase.storage
    .from("farmer-media")
    .upload(storagePath, audioBlob, {
      cacheControl: "3600",
      upsert: false,
      contentType: audioBlob.type || `audio/${format}`,
    });

  if (error) {
    return { path: null, publicUrl: null, signedUrl: null, error };
  }

  const { data: signedData } = await supabase.storage
    .from("farmer-media")
    .createSignedUrl(storagePath, 7200);

  return {
    path: data.path,
    publicUrl: null,
    signedUrl: signedData?.signedUrl ?? null,
    error: null,
  };
}

