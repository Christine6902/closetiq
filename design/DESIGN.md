# DESIGN.md — ClosetIQ

## Project
ClosetIQ is a smart digital wardrobe and outfit planner — it digitises a user's clothing and recommends coordinated outfits by weather, style and occasion. It serves fashion-conscious individuals, busy professionals, students and frequent travellers.

**Scope:** Full — DESIGN.md + brand-guidelines.html + ui-guide.html
**Status:** FINAL (logo supplied) — foundation locked, deliverables in progress.

## Logo
- File: `design/closetiq-logo.png` (referenced as `<img>` in deliverables)
- Colours extracted (from the PNG, quantised): `#F7F2ED` cream ground (94.6%), `#B49669` antique gold, `#1E1E1D` charcoal, plus gold highlights `#C4A678` / `#CCB592` / `#D8C7AE`
- Mark type: icon + wordmark + tagline (a clothes-hanger inside a rounded-square frame above "IQ"; "ClosetIQ" serif wordmark; tagline "YOUR STYLE. SMARTER EVERY DAY.")
- Geometry: typographic + line-icon (hanger drawn in a single fine stroke)
- Weight: fine / elegant line work; high-contrast serif wordmark
- Iconographic motif: clothes hanger in a rounded-square frame — the reusable brand symbol
- Square-safe icon mark: yes — the hanger-in-frame is separable from the wordmark and works as a favicon/app icon

## Favicon Brief
- Icon mark: the hanger-in-rounded-frame symbol from the logo (drop the wordmark)
- Light background: `#F7F2ED`  ·  Icon colour on light: `#1E1E1D` (hanger) with `#B49669` frame
- Dark background: `#1E1E1D`   ·  Icon colour on dark: `#C9AC7C` gold
- Format preference: SVG with `@media (prefers-color-scheme: dark)` embedded; PNG + Apple touch icon fallback
- App name: ClosetIQ
- RFG package: pending — run tina4-seo to generate

## Market Research

### Sector overview
Consumer fashion-lifestyle tech — the "digital wardrobe / outfit planner" app category (Whering, Acloset, Stylebook, Cladwell, Indyx, Fits). ClosetIQ serves style-conscious consumers who want daily outfit help from clothes they already own.

### Competitor landscape
| Brand | Palette category | Typeface category | Visual register |
|-------|-----------------|-------------------|----------------|
| Whering | Bright, playful, community | Rounded sans | Playful-consumer; reviewers note it can look "a bit outdated" |
| Acloset | Clean gallery / Instagram-feed | Sans | Visual, social, photo-led |
| Stylebook | Spare monochrome | Plain sans | Utilitarian, control-first |
| Cladwell | Minimal, muted | Sans | Mindful-minimalist, anti-overwhelm |
| Fits | Clean, light | Sans | Pleasant, understated utility |

### Industry visual conventions
The category splits two ways: playful-consumer (bright, flat, community) and spare-utility (monochrome, control-first). Almost all use flat app-UI colour and geometric/rounded sans type. None occupy the premium, editorial, boutique end of the market.

### Design thesis
The digital-wardrobe sector leans either playful-consumer or spare-utilitarian — flat, bright app colour. ClosetIQ should sit deliberately upmarket as a *personal-stylist boutique*: cream, antique gold and serif typography signalling curated styling intelligence, not inventory tracking — because that premium register is unclaimed in the category and matches the product's "smarter every day" styling promise.

### Motion personality
ClosetIQ motion is refined — transitions are gentle and unhurried, like turning the page of a lookbook. Bias to `--duration-base`/`--duration-slow` and `--ease-in-out`. Never bouncy, never abrupt; no spring easing.

### Colour direction
Anchored entirely to the logo: a warm cream ground, antique-gold accent, and charcoal text. This is the premium-boutique palette — warm neutrals over the cool greys and bright primaries the competition uses. Gold is a decorative/fill accent (it fails as small text on cream), so a darker "accent-strong" gold carries any gold text.

### Typography direction
- **Display: Cormorant Garamond** — an elegant high-contrast Garamond that echoes the serif wordmark; carries the editorial-luxury personality at large sizes.
- **Body / UI: Jost** — a geometric sans (Futura lineage) that matches the logo's spaced-caps tagline; quiet and legible so the serif and gold carry the character.
This serif-display + geometric-sans pairing is a classic luxury combination and directly mirrors the logo lockup. Both are on Google Fonts.

### Icon system
- Library: Lucide (https://lucide.dev)
- Stroke weight in use: 1.5px
- Size tokens: --icon-xs 14px · --icon-sm 16px · --icon-md 20px · --icon-lg 24px · --icon-xl 32px
- Rationale: a fine 1.5px line weight complements the delicate serif and the hanger mark's fine stroke without competing with it.
- Production integration: CDN script `https://unpkg.com/lucide@latest` + `<i data-lucide="name">` then `lucide.createIcons()`. In `ui-guide.html` icons are inline `<svg>` for a dependency-free reference.

## Design Tokens

### Colour — light theme
| Token | Hex | Role |
|-------|-----|------|
| --accent | #B49669 | Antique gold — fills, borders, logo echo, primary-button background (decorative, NOT small text) |
| --accent-hover | #A2875F | Gold darkened ~10% for hover |
| --accent-active | #907854 | Gold darkened ~20% for pressed |
| --accent-tint | #EFE6D5 | Pale gold background — selected rows, highlights |
| --accent-strong | #7A5E34 | Darker gold that PASSES as text/links/labels on cream (5.43:1) |
| --dark | #1E1E1D | Charcoal — primary text, dark surfaces, primary-button text on gold |
| --bg | #F7F2ED | Warm cream linen — page background |
| --surface | #FDFBF8 | Warm near-white — cards, panels, inputs |
| --surface-2 | #F1E9DD | Warm sand — table stripes, sidebar, inset surfaces |
| --border | #E6DDCF | Warm divider / input border |
| --border-strong | #D8C7AE | Focused separators, stronger borders |
| --text-1 | #1E1E1D | Headings, high-emphasis text (15.0:1 on bg) |
| --text-2 | #4A453E | Body copy, labels (8.5:1 on bg) |
| --text-3 | #8A8177 | Captions, placeholders, metadata (3.4:1 — large/non-essential only) |

### Colour — dark theme
| Token | Hex | Notes |
|-------|-----|-------|
| --bg | #1B1A18 | Deep warm charcoal |
| --surface | #252320 | |
| --surface-2 | #2E2B27 | |
| --border | #3A362F | |
| --accent | #C9AC7C | Lighter gold for contrast on dark (8.0:1) |
| --accent-strong | #D8BE91 | Gold text on dark |
| --text-1 | #F4EEE4 | Warm cream text (15.1:1 on dark bg) |
| --text-2 | #C9C1B3 | |
| --text-3 | #938B7E | |

### Semantic colours (contrast-verified on cream; white text on each fill passes ≥4.5)
| Role | Token | Light hex | On cream | Dark hex |
|------|-------|-----------|----------|----------|
| Success | --success | #466038 | 6.3:1 ✓ | #8FB07A |
| Warning | --warning | #8C5200 | 5.7:1 ✓ (burnt umber — shifted off gold) | #D79A4A |
| Error | --error | #AF3A2C | 5.5:1 ✓ | #E0796B |
| Info | --info | #4A6E8A | 4.9:1 ✓ | #8FB4D1 |

Warning is deliberately burnt umber, NOT gold, because the brand accent is gold — a gold "warning" would be invisible as a caution signal. Tint tokens (`--success-tint` etc.) are the semantic colour at ~10% over cream, defined explicitly in CSS.

### Typography
| Role | Token | Family | Weight(s) | clamp() value | Notes |
|------|-------|--------|-----------|---------------|-------|
| Display | --text-display | Cormorant Garamond | 600 | clamp(2.75rem, 2rem + 4vw, 5rem) | −0.02em, lh 1.0 |
| H1 | --text-h1 | Cormorant Garamond | 600 | clamp(2rem, 1.5rem + 2.5vw, 3.5rem) | lh 1.1 |
| H2 | --text-h2 | Cormorant Garamond | 600 | clamp(1.5rem, 1.1rem + 1.6vw, 2.25rem) | lh 1.2 |
| H3 | --text-h3 | Jost | 600 | clamp(1.05rem, 0.9rem + 0.75vw, 1.4rem) | sans at UI heading sizes where the serif gets delicate |
| Overline | --text-overline | Jost | 600 | clamp(0.65rem, 0.6rem + 0.25vw, 0.75rem) | +0.18em, uppercase (tagline style) |
| Body Large | --text-body-lg | Jost | 400 | clamp(1.05rem, 1rem + 0.25vw, 1.15rem) | lh 1.65 |
| Body | --text-body | Jost | 400 | clamp(0.9rem, 0.85rem + 0.25vw, 1rem) | lh 1.6, max 65ch |
| Caption | --text-caption | Jost | 400 | clamp(0.72rem, 0.7rem + 0.1vw, 0.8rem) | lh 1.5 |
| Code | --text-code | ui-monospace | 400 | clamp(0.75rem, 0.72rem + 0.15vw, 0.85rem) | system mono (no SKUs prominent) |

Viewport anchors: min 320px · max 1280px. Display/H1/H2 use the serif; H3 and all UI labels use Jost (the serif thins out below ~1.4rem).

### Form tokens (aliases)
--label-color → --text-2 · --label-color-focused → --accent-strong · --label-color-error → --error · --label-color-disabled → --text-3
--input-bg → --surface · --input-bg-disabled → --surface-2 · --input-border → --border · --input-border-hover → --border-strong · --input-border-focused → --accent-strong · --input-border-error → --error · --placeholder-color → --text-3 · --helper-color → --text-3 · --helper-color-error → --error

### Interaction tokens
| Token | Value |
|-------|-------|
| --focus-ring | 0 0 0 3px var(--accent-tint), 0 0 0 1px var(--accent-strong) |
| --focus-ring-offset | 2px |
| --disabled-opacity | 0.45 |
| --hover-tint | rgba(180, 150, 105, 0.08) |

### Animation tokens
--duration-fast 100ms · --duration-base 200ms · --duration-slow 350ms
--ease-out cubic-bezier(0.2,0,0,1) · --ease-in-out cubic-bezier(0.4,0,0.2,1) · (no --ease-spring — refined brand)
Wrapped in `@media (prefers-reduced-motion: reduce)` → all durations 0ms.

### Z-index scale
base 1 · dropdown 100 · sticky 200 · topbar 300 · drawer 400 · modal-backdrop 500 · modal 600 · toast 700 · tooltip 800

### Spacing scale
4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64 · 80 · 96 px (--space-5 = 20px defined)

### Layout width tokens
--max-prose 65ch · --max-content 720px · --max-wide 1200px

### Border radius
sm 4px · md 8px · lg 16px · full 999px (soft, elegant — echoes the logo's rounded-square frame)

### Shadows (warm-tinted — base rgba(60,45,30,…))
sm: 0 1px 2px rgba(60,45,30,0.08)
md: 0 6px 20px rgba(60,45,30,0.10)
lg: 0 18px 48px rgba(60,45,30,0.16)
Dark mode: switch to pure rgba(0,0,0,…) — warm shadow is invisible on a warm-dark ground.

### Contrast pairs (verified, computed — not eyeballed)
| Text token | Background | Ratio | Pass? |
|-----------|-----------|-------|-------|
| --text-1 #1E1E1D | --bg #F7F2ED | 15.0:1 | ✓ |
| --text-2 #4A453E | --bg | 8.5:1 | ✓ |
| --text-3 #8A8177 | --bg | 3.4:1 | ✓ (≥3:1, large/non-essential) |
| --text-1 | --surface #FDFBF8 | 16.2:1 | ✓ |
| --accent #B49669 (as text) | --bg | 2.5:1 | ✗ → use --accent-strong |
| --accent-strong #7A5E34 | --bg | 5.4:1 | ✓ |
| white | --accent (button) | 2.8:1 | ✗ → gold buttons use charcoal text |
| charcoal #1E1E1D | --accent (button) | 6.0:1 | ✓ |
| --success #466038 | --bg | 6.3:1 | ✓ |
| --warning #8C5200 | --bg | 5.7:1 | ✓ |
| --error #AF3A2C | --bg | 5.5:1 | ✓ |
| --info #4A6E8A | --bg | 4.9:1 | ✓ |
| dark --text-1 #F4EEE4 | dark --bg #1B1A18 | 15.1:1 | ✓ |
| dark --accent #C9AC7C | dark --bg | 8.0:1 | ✓ |

## Reconciliation — placeholder → final (logo supplied 2026-10-08)
The app's current `closetiq.scss` uses a provisional purple/pink palette that CONFLICTS with the supplied logo. Every brand colour changes. The deliverables use the final palette above; applying it to the live app's SCSS is a separate, confirmed step.

| Token | Provisional (in app now) | Final (from logo) |
|-------|--------------------------|-------------------|
| --accent / $primary | #7C5CFF purple | #B49669 gold (text: #7A5E34) |
| secondary / $accent | #EC4899 pink | gold tints #C4A678 / #D8C7AE |
| --bg | #FAF9FC cool white | #F7F2ED warm cream |
| --ink / --dark | #1E1B2E | #1E1E1D charcoal |
| buttons | purple bg + white text | gold bg + charcoal text |

## Next Steps
- SEO/AISO implementation: run tina4-seo (reads this file as source of truth)
- Apply final palette to the live app: update `src/scss/closetiq.scss` tokens + regenerate PWA icons from the real hanger mark (awaiting confirmation)
- WCAG 2.1 AA audit after implementation

## Rationale log
- 2026-10-08: Anchored palette to supplied logo (cream/gold/charcoal), retiring the purple/pink placeholder — the logo is the brand and the two conflict.
- 2026-10-08: Gold reserved for fills/borders; `--accent-strong #7A5E34` introduced for gold text (gold #B49669 only 2.5:1 on cream).
- 2026-10-08: Primary buttons use charcoal text on gold (white fails 2.8:1; charcoal passes 6.0:1).
- 2026-10-08: Warning shifted to burnt umber #8C5200 — a gold warning on a gold-accent brand is not legible as caution.
- 2026-10-08: Type pairing Cormorant Garamond (display) + Jost (UI) to mirror the serif wordmark + geometric-caps tagline; H3/labels use Jost because Cormorant thins out below ~1.4rem.
- 2026-10-08: Motion set to refined/unhurried (no spring) and icons to Lucide 1.5px to match the premium register and the logo's fine line work.
