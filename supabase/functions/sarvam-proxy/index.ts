// ============================================================================
// KisanSamvaad Supabase Edge Function: Sarvam AI Secure API Gateway
// File: supabase/functions/sarvam-proxy/index.ts
// Runtime: Deno / TypeScript (Supabase Edge Network)
// ============================================================================

import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.39.0";

const corsHeaders: Record<string, string> = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
};

interface SarvamProxyPayload {
  action: "speech-to-text" | "text-to-speech" | "translate" | "chat";
  payload: Record<string, unknown>;
}

serve(async (req: Request) => {
  // 1. Handle HTTP OPTIONS Preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    // 2. Validate Supabase Auth Token
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) {
      return new Response(
        JSON.stringify({
          error: "Unauthorized",
          message: "Missing Authorization header containing Supabase JWT",
        }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const supabaseUrl = Deno.env.get("SUPABASE_URL") ?? "";
    const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY") ?? "";
    const sarvamApiKey = Deno.env.get("SARVAM_API_KEY") ?? "";

    if (!sarvamApiKey) {
      return new Response(
        JSON.stringify({
          error: "ConfigurationError",
          message: "SARVAM_API_KEY secret is not provisioned in Supabase Edge environment",
        }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Authenticate user via Supabase Auth
    const supabase = createClient(supabaseUrl, supabaseAnonKey, {
      global: { headers: { Authorization: authHeader } },
    });

    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return new Response(
        JSON.stringify({
          error: "Unauthorized",
          message: "Invalid or expired Supabase JWT session token",
        }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // 3. Parse Request Payload
    const contentType = req.headers.get("content-type") || "";
    let action = "text-to-speech";
    let sarvamUrl = "https://api.sarvam.ai/text-to-speech";
    let forwardHeaders: Record<string, string> = {
      "api-subscription-key": sarvamApiKey,
    };
    let forwardBody: BodyInit | null = null;

    if (contentType.includes("multipart/form-data")) {
      // Audio transcription proxying (Saaras ASR)
      action = "speech-to-text";
      sarvamUrl = "https://api.sarvam.ai/speech-to-text";
      forwardBody = await req.formData();
      // Notice: Do not set Content-Type header manually for FormData; fetch will add boundary automatically
    } else {
      const body: SarvamProxyPayload = await req.json();
      action = body.action;
      forwardHeaders["Content-Type"] = "application/json";

      if (action === "text-to-speech") {
        sarvamUrl = "https://api.sarvam.ai/text-to-speech";
        forwardBody = JSON.stringify(body.payload);
      } else if (action === "translate") {
        sarvamUrl = "https://api.sarvam.ai/translate";
        forwardBody = JSON.stringify(body.payload);
      } else if (action === "chat") {
        sarvamUrl = "https://api.sarvam.ai/chat";
        forwardBody = JSON.stringify(body.payload);
      } else {
        return new Response(
          JSON.stringify({ error: "BadRequest", message: `Unsupported action: ${action}` }),
          { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }
    }

    // 4. Secure Backend Request to Sarvam AI with Masked Key
    const startTime = Date.now();
    const sarvamResponse = await fetch(sarvamUrl, {
      method: "POST",
      headers: forwardHeaders,
      body: forwardBody,
    });

    const latencyMs = Date.now() - startTime;
    const responseData = await sarvamResponse.text();

    return new Response(responseData, {
      status: sarvamResponse.status,
      headers: {
        ...corsHeaders,
        "Content-Type": sarvamResponse.headers.get("content-type") || "application/json",
        "X-Proxied-By": "KisanSamvaad-Supabase-Edge",
        "X-Latency-Ms": latencyMs.toString(),
      },
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Internal proxy error occurred";
    return new Response(
      JSON.stringify({ error: "InternalError", message }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
