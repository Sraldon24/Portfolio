# Frontend Redesign — Amber CRT Terminal + Glassmorphism
**Date:** 2026-03-07
**Status:** Approved

---

## Vision

A dark, cinematic portfolio with the warmth of an old amber CRT monitor glowing in a dark room. Near-black background, amber phosphor glow, frosted glass cards with warm tints. Terminal boot-sequence hero. Everything currently in the site stays — sections are reorganized and merged for a tighter, more intentional flow.

**Reference image:** Old amber CRT monitor on a dark desk, warm orange light radiating outward. That glow, that warmth, that contrast — applied to a modern glassmorphism layout.

---

## Palette

| Token | Value | Usage |
|-------|-------|-------|
| `bg-base` | `#0a0800` | Page background (near-black, warm tint) |
| `bg-surface` | `#120e00` | Section alternates |
| `amber-500` | `#f59e0b` | Primary accent, headings |
| `amber-400` | `#fbbf24` | Interactive, links, highlights |
| `amber-600` | `#d97706` | Borders, dividers |
| `amber-glow` | `#ea580c` | Box shadows, glow halos |
| `text-primary` | `#fde68a` | Body text |
| `text-muted` | `#92400e` | Secondary text, timestamps |
| `glass-bg` | `rgba(245,158,11,0.04)` | Card backgrounds |
| `glass-border` | `rgba(245,158,11,0.15)` | Card borders |

---

## Typography

- **Headings:** `JetBrains Mono` or `Space Mono` — monospace, terminal feel
- **Body:** `Inter` — clean, readable, no compromise
- **Labels/tags:** `JetBrains Mono` small caps
- **Section markers:** `> ` prefix on section titles (terminal prompt style)

---

## New Section Structure

Current sections are **reorganized into 4 zones**, nothing removed:

### Zone 1 — BOOT (Hero)
**Replaces:** Hero section
**Content:** Terminal boot sequence animation + profile photo in CRT bezel frame

Layout:
- Full viewport height
- Dark background with amber glow radiating from center-bottom (like the reference image)
- Left: Terminal boot text types out line by line:
  ```
  > Initializing portfolio...
  > Loading Amir Sraldon
  > Role: [your title]
  > Status: Available for work
  > Languages: EN / FR
  ```
- Right: Profile photo inside a "monitor bezel" — rounded rect frame with amber inner glow, subtle scanline overlay on the *frame only* (not the photo), warm light spilling outward
- Below: Download Resume + Get in Touch CTAs styled as terminal commands `[ ./resume.pdf ]` `[ ./contact ]`

### Zone 2 — SYSTEM INFO (About + Skills merged)
**Replaces:** Skills section (About is currently in hero bio)
**Content:** Bio paragraph + skills grid side by side

Layout:
- Two-column: Left = bio text in a glass terminal card, Right = skills as a live terminal readout
- Skills rendered as `skill_name ████████░░ 80%` — ASCII progress bars instead of CSS bars
- Section header: `> system.info`
- Scroll-triggered: skill bars "fill" like a loading sequence

### Zone 3 — PROJECTS (unchanged content, new card style)
**Replaces:** Projects section
**Content:** Same projects data

Layout:
- Bento grid (not uniform 3-col) — featured project gets a 2x card, others are 1x
- Cards: glass with amber border, hover reveals amber glow
- Project image gets a warm amber color-grade overlay on hover
- Tech tags styled as terminal badges `[python]` `[django]`
- Section header: `> projects.list`

### Zone 4 — TIMELINE (Experience + Education merged)
**Replaces:** Experience & Education sections
**Content:** Both timelines merged into a single unified timeline

Layout:
- Single vertical timeline, alternating left/right
- Experience nodes: amber `●` dot, blue tint label
- Education nodes: amber `◆` dot, emerald tint label
- Timeline line is amber/orange gradient
- Dates styled as terminal timestamps `[2022-01]`
- Section header: `> career.log`

### Zone 5 — HUMAN (Hobbies)
**Replaces:** Hobbies section
**Content:** Same hobbies data

Layout:
- Grid of icon cards, same as now but restyled
- Section header: `> human.exe`
- Cards: glass with amber glow on hover, icons in amber
- Subtle: "// not just a developer" comment text above

### Zone 6 — SOCIAL PROOF (Testimonials)
**Replaces:** Testimonials section
**Content:** Same testimonials + submission form (currently separate, now merged)

Layout:
- Approved testimonials in horizontal scroll (marquee/carousel) or masonry
- Submission form collapsed behind a `> leave_testimonial()` button that expands inline
- Section header: `> reviews.log`

### Zone 7 — CONTACT (unchanged content, restyled)
**Replaces:** Contact section
**Content:** Same contact form + info

Layout:
- Full-width terminal card
- Contact info sidebar replaced with a `whois amir` terminal output block
- Form fields styled as terminal inputs with `> ` cursor prefix
- Submit button: `[ send_message() ]`
- Section header: `> contact.init`

---

## Global UI Patterns

### Navigation
- Fixed top bar: `bg-black/80 backdrop-blur` with amber bottom border (1px glow)
- Nav links: monospace, `> about` style on hover
- Language switcher: `[EN]` `[FR]` terminal toggle style
- Mobile: hamburger → full-screen overlay with large terminal-style links

### Glass Cards
```css
background: rgba(245, 158, 11, 0.04);
border: 1px solid rgba(245, 158, 11, 0.15);
box-shadow: 0 0 20px rgba(234, 88, 12, 0.08);
backdrop-filter: blur(12px);
```
Hover state adds: `box-shadow: 0 0 40px rgba(234, 88, 12, 0.2)`

### Ambient Glow Effect
- Page-level: radial gradient from `#ea580c` at 5% opacity centered bottom-center
- Gives the "CRT in a dark room" feel across the whole page

### Scanline Texture
- CSS `::before` pseudo-element on hero only
- `repeating-linear-gradient` with 2px transparent lines, 3% opacity
- Applied to the monitor bezel frame, NOT to text content

### Section Dividers
- Replace current `section-divider` with a terminal-style separator:
  `─────────────── // ───────────────` in amber at low opacity

### Scroll Animations
- Keep existing fade-in/stagger pattern
- Add: text generation effect on section headers (characters appear one by one)

---

## What Stays Identical (Backend/Django)
- All Django template variables: `{{ profile }}`, `{{ skills }}`, `{{ projects }}`, etc.
- All form logic: contact form, testimonial form, CSRF
- All i18n: `{% trans %}` tags, language switcher
- All model data structures
- Tailwind + custom CSS approach (no new JS frameworks)

---

## Files to Change
- `main/templates/main/base.html` — nav, footer, global styles
- `main/templates/main/home.html` — full restructure into 7 zones
- `main/static/css/input.css` — new custom CSS (amber palette, glass, scanlines, terminal effects)
- `tailwind.config.js` — add amber CRT color tokens, new font families

## Files NOT to Change
- All Python/Django files
- All migration files
- All translation files
- `main/views.py`, `main/models.py`, `main/urls.py`

---

## Open Questions (resolved)
- ✅ Aesthetic: Amber CRT terminal + glassmorphism
- ✅ Hero: A+C hybrid (terminal boot text + CRT bezel photo frame)
- ✅ Structure: Full restructure, nothing removed
- ✅ Color: Amber/orange (#f59e0b primary)
- ✅ Stack: Django templates + Tailwind CSS (no framework change)
