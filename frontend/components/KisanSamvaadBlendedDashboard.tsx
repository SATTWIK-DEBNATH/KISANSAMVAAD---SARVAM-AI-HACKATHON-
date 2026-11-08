import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

/**
 * ============================================================================
 * KISANSAMVAAD BLENDED FRONTEND ARCHITECTURE
 * Blending Three Paradigms:
 * 1. Spikes Language App: Cognitive load reduction, gamified badges, tactile cards.
 * 2. Sarvam AI: Enterprise trust, structured data tables, status pills, voice playground.
 * 3. MDS Collective: Luxury authority, full-bleed imagery, live monitoring ticker.
 *
 * ACCESSIBILITY & ERGONOMICS:
 * - WCAG AAA 7:1 contrast compliance in "Field Mode" (AMOLED #000000 / Stark #FFFFFF / UT Dallas Orange #c95100).
 * - Minimum line-height 1.625 to prevent Brahmic script matra clipping (Noto Sans).
 * - Multi-sensor acoustic error-recovery guidance for noisy farm environments.
 * ============================================================================
 */

// ----------------------------------------------------------------------------
// SVG ICONS (Self-contained to eliminate external icon dependency failures)
// ----------------------------------------------------------------------------
const MicIcon = ({ className = "w-6 h-6" }: { className?: string }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
  </svg>
);

const VolumeIcon = ({ className = "w-5 h-5" }: { className?: string }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
  </svg>
);

const CameraIcon = ({ className = "w-6 h-6" }: { className?: string }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);

const ShieldAlertIcon = ({ className = "w-5 h-5" }: { className?: string }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
  </svg>
);

const AwardIcon = ({ className = "w-5 h-5" }: { className?: string }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
  </svg>
);

const PhoneCallIcon = ({ className = "w-5 h-5" }: { className?: string }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
  </svg>
);

// ----------------------------------------------------------------------------
// DATA DEFINITIONS & MOCK ENTERPRISE REGISTRY
// ----------------------------------------------------------------------------
interface MandiRow {
  id: string;
  crop: string;
  market: string;
  modalPrice: number;
  trendPct: number;
  direction: "up" | "down" | "flat";
  arrivalVolume: string;
}

const MANDI_DATA: MandiRow[] = [
  { id: "1", crop: "Tomato (Hybrid)", market: "Kolar, KA", modalPrice: 1850, trendPct: 6.8, direction: "up", arrivalVolume: "4,200 Qtl" },
  { id: "2", crop: "Onion (Nashik Red)", market: "Yeshwanthpur, KA", modalPrice: 2400, trendPct: -3.2, direction: "down", arrivalVolume: "1,850 Qtl" },
  { id: "3", crop: "Ragi (Indaf-5)", market: "Mandya, KA", modalPrice: 3850, trendPct: 1.5, direction: "up", arrivalVolume: "920 Qtl" },
  { id: "4", crop: "Cotton (DCH-32)", market: "Raichur, KA", modalPrice: 7100, trendPct: -1.1, direction: "down", arrivalVolume: "3,100 Qtl" }
];

export const KisanSamvaadBlendedDashboard: React.FC = () => {
  // --------------------------------------------------------------------------
  // STATE MANAGEMENT
  // --------------------------------------------------------------------------
  const [fieldMode, setFieldMode] = useState<boolean>(true); // Default to AMOLED Field Mode
  const [activeTab, setActiveTab] = useState<"prices" | "weather" | "diagnostics">("prices");
  const [voiceState, setVoiceState] = useState<"idle" | "listening" | "processing" | "speaking" | "noisy">("idle");
  const [transcript, setTranscript] = useState<string>("'ನನಗೆ 2 ಎಕರೆ ಟೊಮೇಟೊ ಬೆಳೆಗೆ ಎಷ್ಟು ಗೊಬ್ಬರ ಬೇಕು?' (Listening for your query...)");
  const [selectedLanguage, setSelectedLanguage] = useState<"kn" | "hi" | "ta" | "en">("kn");
  const [showLangModal, setShowLangModal] = useState<boolean>(false);
  const [communityPoints, setCommunityPoints] = useState<number>(350);

  // Simulated voice state transition
  const handleMicClick = () => {
    if (voiceState === "idle") {
      setVoiceState("listening");
      setTranscript("Listening carefully to ambient farm speech...");
      setTimeout(() => {
        setVoiceState("processing");
        setTranscript("Transcribing via Sarvam Saaras-v4 Indic acoustic model...");
      }, 3000);
      setTimeout(() => {
        setVoiceState("speaking");
        setTranscript("Sarvam Bulbul TTS: '2 ಎಕರೆ ಟೊಮೇಟೊಗೆ 4 ಚೀಲ ಡಿಎಪಿ, 2 ಚೀಲ ಎಸ್ಎಸ್ಪಿ, 6 ಚೀಲ ಯೂರಿಯಾ...'");
      }, 5500);
    } else {
      setVoiceState("idle");
      setTranscript("Tap the microphone or press 1 on telephone keypad to ask.");
    }
  };

  return (
    <div
      className={`min-h-screen w-full transition-colors duration-300 font-sans ${
        fieldMode
          ? "bg-black text-white selection:bg-orange-600 selection:text-black"
          : "bg-[#F7F5F0] text-[#111827] selection:bg-emerald-800 selection:text-white"
      }`}
      style={{
        lineHeight: "1.65" // Enforces line-height 1.65 to ensure Brahmic script modifiers never overlap
      }}
    >
      {/* 
        =======================================================================
        1. MDS COLLECTIVE INFLUENCE: LIVE REAL-TIME STATUS TICKER
        Authoritative luxury agency dashboard aesthetic translated to rural oversight.
        Pulsing status LED + 15km perimeter active surveillance ticker.
        =======================================================================
      */}
      <header className="sticky top-0 z-50 w-full border-b border-neutral-800 bg-black/95 backdrop-blur-md px-3 py-2 text-xs">
        <div className="mx-auto flex max-w-md items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
            <span className="font-mono font-bold tracking-wider text-emerald-400 uppercase">
              LIVE MONITORING [15KM RADIUS]
            </span>
          </div>

          <div className="flex items-center space-x-2">
            {/* Field Mode Ergonomic High-Contrast Toggle */}
            <button
              onClick={() => setFieldMode(!fieldMode)}
              className="rounded border border-neutral-700 bg-neutral-900 px-2 py-0.5 font-mono text-[10px] text-neutral-300 hover:text-white"
              title="Toggle AMOLED Field Mode for direct sunlight legibility"
            >
              {fieldMode ? "FIELD: ON (21:1)" : "STANDARD"}
            </button>

            {/* Language Quick-Switch Pill */}
            <button
              onClick={() => setShowLangModal(true)}
              className="rounded border border-orange-500/80 bg-orange-950/40 px-2 py-0.5 font-bold text-orange-400"
            >
              {selectedLanguage === "kn" ? "ಕನ್ನಡ" : selectedLanguage === "hi" ? "हिन्दी" : selectedLanguage === "ta" ? "தமிழ்" : "ENG"}
            </button>
          </div>
        </div>

        {/* MDS Scrolling Alert Sub-ticker */}
        <div className="mx-auto mt-1 max-w-md overflow-hidden whitespace-nowrap text-[11px] text-neutral-400">
          <div className="inline-block animate-marquee font-mono">
            KOLAR DISTRICT: No Spodoptera outbreak detected - Next rain window: 48h (Low Risk) - Urea statutory stock at Primary PACS: 420 Bags.
          </div>
        </div>
      </header>

      {/* MAIN CONTAINER: Constrained to standard 360px - 430px smartphone viewport */}
      <main className="mx-auto max-w-md px-4 pb-24 pt-3">
        
        {/* 
          =====================================================================
          SPIKES EDTECH INFLUENCE: USER REPUTATION & AGRI-STACK IDENTITY
          Soft tactile card, points accumulation, and verified farmer credential.
          =====================================================================
        */}
        <section className="mb-4 rounded-2xl border border-neutral-800 bg-gradient-to-r from-neutral-900 to-neutral-950 p-3 shadow-md">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-[11px] font-mono uppercase tracking-wider text-neutral-400">
                AgriStack Verified Farmer
              </div>
              <h1 className="text-base font-bold text-white">
                Manjunath K. <span className="text-xs font-normal text-emerald-400 font-mono">(FID-KA-98412)</span>
              </h1>
              <p className="text-xs text-neutral-400">
                Malur, Kolar - 2.0 Acres (Tomato & Ragi)
              </p>
            </div>

            {/* Spikes Gamification Badge */}
            <div className="flex flex-col items-end">
              <div className="flex items-center space-x-1 rounded-full border border-orange-500/40 bg-orange-950/60 px-2.5 py-1 text-orange-300">
                <AwardIcon className="h-4 w-4 text-orange-400" />
                <span className="font-mono text-xs font-bold">+{communityPoints}</span>
              </div>
              <span className="mt-1 text-[10px] text-neutral-400 font-medium">Level 3 Krishi Mitra</span>
            </div>
          </div>
        </section>

        {/* 
          =====================================================================
          THE GLOBAL HERO / VOICE PLAYGROUND (MDS + SARVAM SYNTHESIS)
          Full-bleed agricultural background, dark authoritative vignette,
          oversized glowing Microphone FAB, and live acoustic waveform.
          =====================================================================
        */}
        <section className="relative mb-5 overflow-hidden rounded-3xl border border-neutral-800 bg-neutral-950 p-6 text-center shadow-2xl">
          {/* MDS Dark Agricultural Canvas Vignette */}
          <div 
            className="absolute inset-0 z-0 bg-cover bg-center opacity-25 filter grayscale contrast-125"
            style={{
              backgroundImage: "radial-gradient(circle at center, rgba(18,63,42,0.8) 0%, rgba(0,0,0,0.95) 100%)"
            }}
          />

          <div className="relative z-10 flex flex-col items-center">
            {/* Status Indicator */}
            <span className="mb-2 rounded-full border border-neutral-700 bg-black/80 px-3 py-1 font-mono text-[10px] font-bold tracking-wider text-neutral-300 uppercase">
              {voiceState === "idle" && "READY TO LISTEN (SARVAM SAARAS-V4)"}
              {voiceState === "listening" && "RECORDING FARMER QUERY..."}
              {voiceState === "processing" && "REASONING WITH ICAR GROUNDING..."}
              {voiceState === "speaking" && "PLAYING BULBUL SYNTHESIZED SPEECH"}
              {voiceState === "noisy" && "ACOUSTIC INTERFERENCE DETECTED"}
            </span>

            {/* MASSIVE GLOWING MICROPHONE FAB */}
            <div className="relative my-4 flex items-center justify-center">
              {/* Outer Pulse Rings for Voice Primacy */}
              <AnimatePresence>
                {voiceState === "listening" && (
                  <motion.div
                    initial={{ scale: 0.9, opacity: 0.8 }}
                    animate={{ scale: 1.45, opacity: 0 }}
                    transition={{ repeat: Infinity, duration: 1.6, ease: "easeOut" }}
                    className="absolute h-28 w-28 rounded-full bg-orange-600/40"
                  />
                )}
              </AnimatePresence>

              <button
                onClick={handleMicClick}
                aria-label="Activate Voice Assistant"
                className={`relative flex h-24 w-24 items-center justify-center rounded-full border-4 shadow-xl transition-all duration-300 active:scale-95 ${
                  voiceState === "listening"
                    ? "border-orange-400 bg-orange-600 text-black shadow-orange-600/50"
                    : voiceState === "speaking"
                    ? "border-emerald-400 bg-emerald-600 text-black shadow-emerald-600/50"
                    : "border-orange-500 bg-gradient-to-b from-orange-500 to-orange-700 text-black hover:border-orange-300"
                }`}
              >
                <MicIcon className="h-10 w-10 stroke-[2.5]" />
              </button>
            </div>

            {/* Framer Motion Interactive Waveform Equalizer (Sarvam Playground Style) */}
            <div className="my-2 flex h-8 items-center justify-center space-x-1.5">
              {[18, 36, 12, 44, 28, 14, 40, 22].map((height, i) => (
                <motion.span
                  key={i}
                  animate={{
                    height: voiceState === "listening" ? [8, height, 10] : voiceState === "speaking" ? [12, height * 0.8, 14] : 4
                  }}
                  transition={{
                    repeat: Infinity,
                    duration: 0.6,
                    delay: i * 0.08,
                    ease: "easeInOut"
                  }}
                  className={`w-1 rounded-full ${
                    voiceState === "listening"
                      ? "bg-orange-400"
                      : voiceState === "speaking"
                      ? "bg-emerald-400"
                      : "bg-neutral-700"
                  }`}
                />
              ))}
            </div>

            {/* Real-time High-Contrast Transcript Fallback Container */}
            <div className="mt-3 w-full rounded-xl border border-neutral-800 bg-black/90 p-3 text-left">
              <div className="flex items-center justify-between text-[10px] font-mono text-neutral-400">
                <span>SPEECH TRANSCRIPT (INDIC ASR)</span>
                {voiceState === "speaking" && (
                  <span className="flex items-center text-emerald-400 font-bold">
                    <VolumeIcon className="mr-1 h-3.5 w-3.5" /> BULBUL:V4-FLASH
                  </span>
                )}
              </div>
              <p className="mt-1 text-sm font-medium leading-relaxed text-white">
                {transcript}
              </p>
            </div>

            {/* HCI Acoustic Error Recovery Banner: Wind Shear / Background Tractor Guidance */}
            {voiceState === "noisy" && (
              <div className="mt-3 flex items-center space-x-2 rounded-lg border border-yellow-600 bg-yellow-950/60 p-2 text-xs text-yellow-200 text-left">
                <ShieldAlertIcon className="h-5 w-5 flex-shrink-0 text-yellow-400" />
                <span>Heavy ambient wind noise detected. Please shield phone or move 5 paces away from tractor.</span>
              </div>
            )}
          </div>
        </section>

        {/* 
          =====================================================================
          CIB&RC REGULATORY SAFETY & TRUST MODULE
          Strict compliance with Indian Pesticide Regulations:
          - No branded pesticide endorsements.
          - Mandatory KVK extension officer human-in-the-loop verification button.
          =====================================================================
        */}
        <section className="mb-5 rounded-2xl border-2 border-red-600/80 bg-red-950/30 p-3.5">
          <div className="flex items-start space-x-2.5">
            <ShieldAlertIcon className="mt-0.5 h-5 w-5 flex-shrink-0 text-red-400" />
            <div className="text-left">
              <span className="rounded bg-red-600 px-1.5 py-0.5 font-mono text-[9px] font-extrabold text-white uppercase">
                CIB&RC MANDATORY SAFETY NOTICE
              </span>
              <p className="mt-1 text-xs font-semibold leading-relaxed text-red-200">
                Generic active formulations only. Banned chemical mixtures (e.g. Endosulfan, Monocrotophos) are strictly prohibited. Always confirm chemical spray dilution with your local university agronomist.
              </p>
              
              {/* Direct KVK Officer Dial Action */}
              <a
                href="tel:18001801551"
                className="mt-2.5 inline-flex items-center justify-center rounded-xl bg-red-600 px-3 py-2 text-xs font-bold text-white shadow-lg hover:bg-red-500 active:scale-95 transition-transform"
              >
                <PhoneCallIcon className="mr-1.5 h-4 w-4" />
                Call KVK Krishi Vigyan Kendra (1800-180-1551)
              </a>
            </div>
          </div>
        </section>

        {/* 
          =====================================================================
          THE HYPERLOCAL DATA DASHBOARD (SARVAM ENTERPRISE INFLUENCE)
          Tabbed navigation, structured tables, status pills with WCAG AAA 
          geometric arrows, and dynamic AI insight callouts.
          =====================================================================
        */}
        <section className="mb-5 rounded-2xl border border-neutral-800 bg-neutral-950 p-4">
          {/* Tab Navigation */}
          <div className="grid grid-cols-3 gap-1 rounded-xl bg-neutral-900 p-1 text-center font-bold text-xs">
            <button
              onClick={() => setActiveTab("prices")}
              className={`rounded-lg py-2 transition-all ${
                activeTab === "prices"
                  ? "bg-black text-white border border-neutral-700 shadow-sm"
                  : "text-neutral-400 hover:text-white"
              }`}
            >
              Mandi Rates
            </button>
            <button
              onClick={() => setActiveTab("weather")}
              className={`rounded-lg py-2 transition-all ${
                activeTab === "weather"
                  ? "bg-black text-white border border-neutral-700 shadow-sm"
                  : "text-neutral-400 hover:text-white"
              }`}
            >
              Weather & Spray
            </button>
            <button
              onClick={() => setActiveTab("diagnostics")}
              className={`rounded-lg py-2 transition-all ${
                activeTab === "diagnostics"
                  ? "bg-black text-white border border-neutral-700 shadow-sm"
                  : "text-neutral-400 hover:text-white"
              }`}
            >
              Soil & Rupee
            </button>
          </div>

          {/* TAB 1: MANDI PRICE TABLE */}
          {activeTab === "prices" && (
            <div className="mt-3">
              <div className="flex items-center justify-between py-1 text-[11px] font-mono text-neutral-400">
                <span>APMC MARKET BENCHMARKS</span>
                <span className="text-emerald-400">AGMARKNET LIVE</span>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="border-b border-neutral-800 text-[10px] uppercase text-neutral-400">
                      <th className="py-2">Commodity</th>
                      <th className="py-2">Mandi Hub</th>
                      <th className="py-2 text-right">Modal Price</th>
                      <th className="py-2 text-right">24h Trend</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-neutral-900">
                    {MANDI_DATA.map((row) => (
                      <tr key={row.id} className="hover:bg-neutral-900/50">
                        <td className="py-2.5 font-bold text-white">{row.crop}</td>
                        <td className="py-2.5 text-neutral-400">{row.market}</td>
                        <td className="py-2.5 text-right font-mono font-bold text-white">
                          ₹{row.modalPrice.toLocaleString()}
                        </td>
                        <td className="py-2.5 text-right">
                          {/* Geometric Status Pill (WCAG AAA contrast independent of color) */}
                          <span
                            className={`inline-flex items-center rounded-md px-1.5 py-0.5 font-mono text-[11px] font-bold ${
                              row.direction === "up"
                                ? "bg-emerald-950 text-emerald-300 border border-emerald-700"
                                : "bg-red-950 text-red-300 border border-red-700"
                            }`}
                          >
                            {row.direction === "up" ? "▲ +" : "▼ "}
                            {Math.abs(row.trendPct)}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Sarvam-Style Dynamic Insight Callout Box */}
              <div className="mt-3.5 rounded-xl border-l-4 border-l-orange-500 border border-neutral-800 bg-neutral-900 p-3 text-left">
                <div className="flex items-center space-x-1.5 text-xs font-bold text-orange-400 font-mono">
                  <span>💡 ICAR-NIAP ECONOMIC FORECAST</span>
                </div>
                <p className="mt-1 text-xs leading-relaxed text-neutral-200">
                  Historical data in Kolar APMC indicates Hybrid Tomato supplies tighten over the next 48 hours. Consider staggering your harvest picking to capture projected <strong>₹120-180/quintal price gains</strong> on Thursday.
                </p>
              </div>
            </div>
          )}

          {/* TAB 2: WEATHER & SPRAY WINDOW (AgriStack Krishi-DSS) */}
          {activeTab === "weather" && (
            <div className="mt-3 space-y-3 text-left">
              <div className="rounded-xl border border-neutral-800 bg-neutral-900 p-3">
                <div className="flex items-center justify-between text-xs font-mono text-neutral-400">
                  <span>MALUR TALUK WEATHER</span>
                  <span className="text-emerald-400">IMD DAMU RADAR</span>
                </div>
                <div className="mt-2 flex items-center justify-between">
                  <div>
                    <div className="text-3xl font-extrabold text-white">28.4°C</div>
                    <div className="text-xs text-neutral-400">Humidity: 68% - Wind: 9.2 km/h</div>
                  </div>
                  <div className="rounded-lg border border-emerald-600 bg-emerald-950/60 p-2 text-center">
                    <span className="font-mono text-xs font-bold text-emerald-300">SPRAY WINDOW</span>
                    <div className="text-[10px] text-emerald-400">SAFE (Wind &lt; 15 km/h)</div>
                  </div>
                </div>
              </div>

              <div className="rounded-xl border border-neutral-800 bg-neutral-900 p-3">
                <span className="font-mono text-xs font-bold text-orange-400">72-HOUR RAIN ADVISORY</span>
                <p className="mt-1 text-xs leading-relaxed text-neutral-200">
                  Precipitation likelihood: <strong>15% (3.2 mm)</strong>. Safe for basal fertilizer soil application. No torrential rain wash-off anticipated before Friday.
                </p>
              </div>
            </div>
          )}

          {/* TAB 3: SOIL & RUPEE PLANNER */}
          {activeTab === "diagnostics" && (
            <div className="mt-3 space-y-3 text-left">
              <div className="rounded-xl border border-neutral-800 bg-neutral-900 p-3">
                <div className="flex items-center justify-between text-xs font-mono text-neutral-400">
                  <span>DETERMINISTIC INTEGER OPTIMIZER</span>
                  <span className="text-orange-400">STATUTORY MRP</span>
                </div>
                <div className="mt-2 text-2xl font-black text-white">₹13,199 <span className="text-xs font-normal text-neutral-400">for 2.0 Acres Tomato</span></div>
                <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
                  <div className="rounded border border-neutral-800 p-1.5">
                    <div className="font-mono text-neutral-400">DAP (50kg)</div>
                    <div className="font-bold text-white">4 Bags (₹5,400)</div>
                  </div>
                  <div className="rounded border border-neutral-800 p-1.5">
                    <div className="font-mono text-neutral-400">SSP (50kg)</div>
                    <div className="font-bold text-white">2 Bags (₹1,100)</div>
                  </div>
                  <div className="rounded border border-neutral-800 p-1.5">
                    <div className="font-mono text-neutral-400">Neem Urea (45kg)</div>
                    <div className="font-bold text-white">6 Bags (₹1,599)</div>
                  </div>
                  <div className="rounded border border-neutral-800 p-1.5">
                    <div className="font-mono text-neutral-400">MOP (50kg)</div>
                    <div className="font-bold text-white">3 Bags (₹5,100)</div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </section>

        {/* 
          =====================================================================
          MULTIMODAL DIAGNOSTICS & GAMIFICATION CARD (SPIKES INFLUENCE)
          Dashed-border dropzone, camera scan visualizer, and reward hooks.
          =====================================================================
        */}
        <section className="relative mb-5 rounded-3xl border border-neutral-800 bg-neutral-950 p-4 text-left shadow-lg">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-white">Crop Doctor & Soil Health OCR</h2>
            <div className="rounded-full border border-orange-500/40 bg-orange-950/70 px-2.5 py-0.5 text-[10px] font-bold text-orange-300">
              Earn +50 Points
            </div>
          </div>

          <p className="mt-1 text-xs text-neutral-400">
            Photograph your physical Soil Health Card or leaf pest symptoms for immediate ICAR diagnostic review.
          </p>

          {/* Spikes Tactile Dashed Upload Dropzone */}
          <div className="mt-3 flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-neutral-700 bg-neutral-900/60 p-6 text-center hover:border-orange-500 cursor-pointer transition-colors">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-neutral-800 text-orange-400 mb-2">
              <CameraIcon className="h-6 w-6" />
            </div>
            <span className="text-xs font-bold text-white">Capture or Upload Photo</span>
            <span className="text-[10px] text-neutral-400 mt-0.5 font-mono">JPG, PNG, or PDF (Auto-enhanced for sunlight glare)</span>
          </div>
        </section>

      </main>

      {/* 
        =======================================================================
        SPIKES MULTILINGUAL SELECTION MODAL
        Oversized tactile cards with native Brahmic scripts and voice previews.
        =======================================================================
      */}
      <AnimatePresence>
        {showLangModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-end justify-center bg-black/80 backdrop-blur-sm p-4 sm:items-center"
          >
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: 50, opacity: 0 }}
              className="w-full max-w-md rounded-3xl border border-neutral-800 bg-neutral-950 p-5 text-left"
            >
              <div className="flex items-center justify-between pb-3 border-b border-neutral-800">
                <h3 className="text-sm font-bold text-white">Select Spoken Language / ಭಾಷೆ ಆಯ್ಕೆ</h3>
                <button
                  onClick={() => setShowLangModal(false)}
                  className="rounded-full bg-neutral-800 px-2 py-1 text-xs text-neutral-400 hover:text-white"
                >
                  ✕
                </button>
              </div>

              <div className="mt-4 grid grid-cols-2 gap-2.5">
                {[
                  { id: "kn", name: "ಕನ್ನಡ", label: "Kannada (Karnataka)" },
                  { id: "hi", name: "हिन्दी", label: "Hindi (North India)" },
                  { id: "ta", name: "தமிழ்", label: "Tamil (Tamil Nadu)" },
                  { id: "en", name: "English", label: "Indian English" }
                ].map((lang) => (
                  <button
                    key={lang.id}
                    onClick={() => {
                      setSelectedLanguage(lang.id as any);
                      setShowLangModal(false);
                      setCommunityPoints(p => p + 10); // Spikes reward loop
                    }}
                    className={`flex flex-col items-start rounded-2xl border p-3.5 transition-all text-left ${
                      selectedLanguage === lang.id
                        ? "border-orange-500 bg-orange-950/40 text-white"
                        : "border-neutral-800 bg-neutral-900 text-neutral-300 hover:border-neutral-700"
                    }`}
                  >
                    <span className="text-xl font-bold leading-normal">{lang.name}</span>
                    <span className="text-[11px] text-neutral-400 mt-1">{lang.label}</span>
                  </button>
                ))}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 
        =======================================================================
        FIXED BOTTOM NAV BAR: DUAL-TOUCH ERGONOMICS
        Large, finger-friendly targets for one-handed outdoor usage.
        =======================================================================
      */}
      <nav className="fixed bottom-0 left-0 right-0 z-40 border-t border-neutral-800 bg-black/95 backdrop-blur-md px-4 py-2">
        <div className="mx-auto flex max-w-md items-center justify-around text-center text-xs font-medium">
          <button
            onClick={() => setActiveTab("prices")}
            className={`flex flex-col items-center py-1 ${activeTab === "prices" ? "text-orange-400 font-bold" : "text-neutral-400"}`}
          >
            <span>Mandi</span>
          </button>
          <button
            onClick={() => setActiveTab("weather")}
            className={`flex flex-col items-center py-1 ${activeTab === "weather" ? "text-orange-400 font-bold" : "text-neutral-400"}`}
          >
            <span>Weather</span>
          </button>
          <button
            onClick={handleMicClick}
            className="flex -mt-5 flex-col items-center justify-center h-12 w-12 rounded-full bg-orange-600 text-black border-2 border-orange-300 shadow-lg active:scale-90"
            aria-label="Mic center"
          >
            <MicIcon className="h-6 w-6" />
          </button>
          <button
            onClick={() => setActiveTab("diagnostics")}
            className={`flex flex-col items-center py-1 ${activeTab === "diagnostics" ? "text-orange-400 font-bold" : "text-neutral-400"}`}
          >
            <span>Soil Plan</span>
          </button>
          <button
            onClick={() => setShowLangModal(true)}
            className="flex flex-col items-center py-1 text-neutral-400 hover:text-white"
          >
            <span>Language</span>
          </button>
        </div>
      </nav>
    </div>
  );
};

export default KisanSamvaadBlendedDashboard;

