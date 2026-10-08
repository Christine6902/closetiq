# Design Plan — ClosetIQ

**Outcome:** A complete visual identity and UI system recorded in design/DESIGN.md and shipped as design/brand-guidelines.html and design/ui-guide.html, anchored to the supplied ClosetIQ logo (cream / antique gold / charcoal serif).

## Scope
- [x] Phase 1: Intake complete — logo supplied (design/closetiq-logo.png), name, about, industry, audience gathered
- [x] Phase 2: Market research complete — sector landscape, colour direction, type pairing, motion personality recorded in DESIGN.md
- [x] Phase 3: Design tokens decided — palette, form tokens, semantic colours (contrast-verified), fluid type scale, spacing, radius, shadows, animation, z-index locked in DESIGN.md
- [x] Phase 4: brand-guidelines.html built and saved to design/ (6 sections: cover, story, logo, colour, type, voice, applications)
- [x] Phase 5: ui-guide.html built and saved to design/ (icons, tokens, type, spacing, responsive, buttons, forms, cards, badges/alerts, nav, progress/states, table, modal/drawer)
- [x] Phase 6: DESIGN.md finalised; both files verified rendering in browser (layout, type, palette, gold+charcoal buttons confirmed)
- [ ] Phase 7: website.html (optional — not requested)

## Bugs
(none)

## Commits
- 2026-10-08: design/DESIGN.md written — full token system anchored to supplied logo; purple/pink placeholder retired.
- 2026-10-08: design/brand-guidelines.html + design/ui-guide.html built from the token system.

## Status: Complete (Phases 1–6)
Note: deliverables reference the logo as `<img src="closetiq-logo.png">` (sits beside them in design/). The in-app preview sandboxes local files as data: URLs so the logo shows broken there; it loads when the file is opened from the design/ folder. Follow-on (confirmed separately): apply the final palette to the live app's src/scss/closetiq.scss and regenerate PWA icons from the hanger mark.
