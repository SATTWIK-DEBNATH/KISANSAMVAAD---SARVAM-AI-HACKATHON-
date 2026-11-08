# KisanSamvaad Design System Specification

## 1. Design Philosophy: "Intelligence That Speaks the Language of the Land"

KisanSamvaad unifies three aesthetic and functional disciplines into one coherent design language:
1. **Editorial Design**: Confident Space Grotesk display typography, deliberate asymmetrical composition, hairline borders, and purposeful narrative pacing inspired by the Foreman craft standards.
2. **Agricultural Tactility**: Grounded in the materials of the land: deep forest foliage, red sandy loam soil, sun-dried harvested grain, and textured paper Soil Health Cards.
3. **Technological Precision**: Sub-second voice waveforms, machine vision bounding boxes, APMC market data grids, and strict ICAR provenance badges.

---

## 2. Color Palette & Token Architecture

The color system uses OKLCH-calculated lightness values to guarantee WCAG 2.2 AA compliance across all light and dark surfaces.

### Primary Surfaces & Identity
- **Deep Forest Green** (`--forest-deep`: `#123F2A`): Primary institutional identity, dark surfaces, authoritative headers. Contrast against white: 11.8:1 (AAA).
- **Agricultural Green** (`--agri-green`: `#236B45`): Primary interactive action color, active buttons, confirmed status. Contrast against white: 5.6:1 (AA).
- **Agricultural Green Hover** (`--agri-green-hover`: `#1B5336`): Interactive hover state.
- **Soft Sage** (`--soft-sage`: `#DCE9DB`): Subtle background tint, secondary badge container, muted highlights.
- **Warm Ivory** (`--warm-ivory`: `#F6F4EC`): Primary card background, secondary section surface, soft paper feel.
- **Paper White** (`--paper-white`: `#FCFBF7`): Foundation background, clean reading ground.

### Supporting & Semantic Tokens
- **Charcoal** (`--charcoal`: `#171B18`): Primary text color on light grounds. Contrast against paper white: 15.4:1 (AAA).
- **Charcoal Card** (`--charcoal-card`: `#18201B`): Secondary card ground on dark cinematic sections.
- **Charcoal Background** (`--charcoal-bg`: `#121815`): Dark section canvas ground.
- **Muted Grey** (`--muted-grey`: `#777D76`): Secondary metadata, captions, inactive borders. Contrast: 4.6:1 (AA).
- **Earth Brown** (`--earth-brown`: `#92765D`): Soil diagnostic accents, organic matter indicators.
- **Harvest Amber** (`--harvest-amber`: `#DCA849`): Signature accent, technical telemetry badges, warning thresholds. Contrast on dark: 8.9:1 (AAA).
- **Error Red** (`--error-red`: `#B3412E`): Restrained warning and banned substance intercept badge. Contrast on white: 5.2:1 (AA).
- **Hairline Border Light** (`--border-hairline`: `rgba(119, 125, 118, 0.22)`): 1px structural dividing lines on light surfaces.
- **Hairline Border Dark** (`--border-dark`: `rgba(252, 251, 247, 0.12)`): 1px structural dividing lines on dark surfaces.

### Surface Distribution Rule (60 / 30 / 10)
- **60% Light Grounds**: Warm Ivory (`#F6F4EC`) and Paper White (`#FCFBF7`) for prolonged reading comfort under sunlight.
- **30% Dark Ground**: Deep Forest Green (`#123F2A`) and Charcoal (`#121815`) for cinematic hero, telephony simulator, and terminal HUDs.
- **10% Accent**: Harvest Amber (`#DCA849`) and Agricultural Green (`#236B45`) for critical focal points only.

---

## 3. Typography Hierarchy

### Type Families
1. **Display Family**: `Space Grotesk` (Google Fonts / local fallback sans-serif).
   - Characterized by technical monospace-inspired curves, open apertures, and strong geometric authority.
   - Used for display headlines, section titles, and monumental numerical metrics.
2. **Body Family**: `Inter` (Google Fonts / local fallback sans-serif).
   - High x-height, neutral letterforms, maximum legibility on low-resolution mobile screens.
   - Used for editorial narrative, card descriptions, data tables, and application UI.
3. **Monospace Technical Family**: `JetBrains Mono` / monospace.
   - Tabular figures (`font-variant-numeric: tabular-nums`), telemetry stamps, citations, code values.
4. **Regional Indic Families**:
   - Kannada: `Noto Sans Kannada`
   - Hindi: `Noto Sans Devanagari`
   - Tamil: `Noto Sans Tamil`
   - Native glyph rendering with explicit line-height >= 1.25 to prevent clipping of vowel signs (matras) and conjuncts (ottu).

### Fluid Type Scale
- **Hero Headline**: `clamp(2rem, 5.5vw, 4.4rem)` | Leading: `1.05` | Tracking: `-0.035em`
- **Section Heading**: `clamp(1.75rem, 3.8vw, 2.75rem)` | Leading: `1.12` | Tracking: `-0.025em`
- **Card Title / Screen Header**: `1.25rem (20px)` | Leading: `1.3` | Tracking: `-0.015em`
- **Body Regular**: `1rem (16px)` | Leading: `1.65` | Max-width: `66ch`
- **Body Small**: `0.875rem (14px)` | Leading: `1.5`
- **Eyebrow Label**: `0.6875rem (11px)` | Tracking: `+0.12em` | Uppercase for Latin text only

---

## 4. Texture System (Tactile Physicality)

The texture system gives the brand an authentic printed paper and agricultural feel without compromising readability or performance.

### Layer A: Global Surface Grain
- Lightweight inline SVG noise filter using `<feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" stitchTiles="stitch"/>`.
- Fixed overlay with `pointer-events: none`, rendered at `3.5%` opacity with CSS blend mode `multiply` on light surfaces and `soft-light` on dark surfaces.
- Memory overhead: zero additional network requests, under 1KB inline CSS/SVG.

### Layer B: Textured Display Type
- Applied strictly to display headings >= 40px (Hero and Section 12).
- Never applied to functional UI labels, buttons, forms, tables, or Indic regional scripts.
- Subtle ink-bleed edge roughness achieved via inline SVG displacement maps that degrade cleanly to solid fill under `forced-colors` or `prefers-reduced-data`.

### Layer C: Material Cues
- Hairline architectural rules (1px borders).
- 48px coordinate background grids representing survey maps and agrometeorological field plots.
- Stamped institutional metadata cards formatted like official ICAR test station bulletins.

---

## 5. Reusable Component Specifications

### 1. Data Provenance Tag (`<span class="provenance-tag">`)
Four strict operational states across all market, soil, and voice outputs:
- `LIVE`: Green chip (`#052E16` on `#4ADE80`), verified timestamp, source entity.
- `CACHED`: Amber chip (`#451A03` on `#FBBF24`), cache age indicator.
- `DEMO`: Blue chip (`#172554` on `#60A5FA`), synthetic dataset notice.
- `UNAVAILABLE`: Red chip (`#450A0A` on `#F87171`), offline fallback mode.

### 2. Primary Voice Trigger (`<button class="mic-btn-main">`)
- Minimum touch target: 80px diameter on desktop, 64px persistent on mobile.
- Ring states: Idle (green glow), Listening (pulsing green), Processing (spinning amber), Error (solid red).
- Keyboard accessible via Spacebar and Enter, with tap-to-toggle and press-and-hold modes.

### 3. Diagnostic Gauge Card (`<div class="gauge-box">`)
- Tabular numeric readout, ICAR rating pill (Low / Medium / High / Acidic), animated proportional fill bar.
- Direct inline editing toggle for manual farmer verification.

### 4. Mandi Rates Data Grid (`<div class="mandi-wrapper">`)
- Horizontal touch-scroll wrapper with sticky headers, commodity badges, and modal price indicators.

### 5. Mobile Application Bottom Navigation (`<nav class="app-bottom-nav">`)
- Fixed bottom dock with 5 core touch destinations: Home, Voice, Soil, Mandi, Weather.
- Touch target height: 60px. Labels >= 11px with icons.
