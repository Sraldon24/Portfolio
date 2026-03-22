# Portfolio Memory
## Rules & Stack
- **Max 5k tokens/response**. No MCP dump in chat. Active MCPs: magic-ui, shadcn.
- Django 6 + django-parler. Vanilla JS + CSS ports of Magic UI effects. Tailwind CSS v3.
- Build: `npm run build:css`. Tests: `main/tests/test_backgrounds.py`. Deploy: Docker.
## Design & 7-Zones
- Terminal, Amber CRT monitor glowing. Fonts: JetBrains Mono, Inter.
- Zones: 1. BOOT 2. SYSTEM INFO 3. PROJECTS 4. CAREER 5. HUMAN 6. SOCIAL PROOF 7. CONTACT
## i18n
- **RULE**: ALL visible strings use `{% trans %}`. Locales: `locale/en/`, `locale/fr/`.
