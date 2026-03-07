# Frontend Redesign — Amber CRT Terminal Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rework the entire portfolio frontend into an amber CRT terminal + glassmorphism aesthetic, restructuring all sections into 7 thematic zones without removing any content or touching any Python/Django files.

**Architecture:** Pure frontend rework — Django templates + Tailwind CSS v3 + vanilla JS. No new dependencies. All existing template variables, form logic, i18n tags, and Django model data stay untouched. Only HTML structure, CSS classes, and inline JS are changed.

**Tech Stack:** Django templates, Tailwind CSS v3 (build: `npm run build:css`), vanilla JS, Google Fonts (JetBrains Mono + Inter)

**Build command:** `npm run build:css` — run after every CSS change to recompile `output.css`

**Dev server:** `python manage.py runserver` from project root with venv activated

---

## Task 1: Tailwind Config + Font Setup

**Files:**
- Modify: `tailwind.config.js`
- Modify: `main/static/css/input.css`

**Step 1: Update tailwind.config.js**

Replace the `theme.extend` section with:

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/**/*.html',
        './main/templates/**/*.html',
        './**/templates/**/*.html',
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                mono: ['"JetBrains Mono"', 'monospace'],
                heading: ['"JetBrains Mono"', 'monospace'],
            },
            colors: {
                crt: {
                    bg: '#0a0800',
                    surface: '#120e00',
                    amber: '#f59e0b',
                    'amber-light': '#fbbf24',
                    'amber-dark': '#d97706',
                    glow: '#ea580c',
                    text: '#fde68a',
                    muted: '#92400e',
                },
            },
            keyframes: {
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-20px)' },
                },
                'glow-pulse': {
                    '0%, 100%': { opacity: '0.6', transform: 'scale(1)' },
                    '50%': { opacity: '1', transform: 'scale(1.05)' },
                },
                'crt-flicker': {
                    '0%, 100%': { opacity: '1' },
                    '92%': { opacity: '1' },
                    '93%': { opacity: '0.8' },
                    '94%': { opacity: '1' },
                    '96%': { opacity: '0.9' },
                    '97%': { opacity: '1' },
                },
                'typing': {
                    from: { width: '0' },
                    to: { width: '100%' },
                },
                'blink': {
                    '0%, 100%': { opacity: '1' },
                    '50%': { opacity: '0' },
                },
                'shine': {
                    '0%': { left: '-100%' },
                    '100%': { left: '200%' },
                },
                'draw-line': {
                    '0%': { height: '0%' },
                    '100%': { height: '100%' },
                },
                'slide-up': {
                    '0%': { opacity: '0', transform: 'translateY(30px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
            },
            animation: {
                'float': 'float 6s ease-in-out infinite',
                'float-slow': 'float 8s ease-in-out infinite',
                'glow-pulse': 'glow-pulse 3s ease-in-out infinite',
                'crt-flicker': 'crt-flicker 8s infinite',
                'blink': 'blink 1s step-end infinite',
                'shine': 'shine 1.5s ease-in-out',
                'draw-line': 'draw-line 1.5s ease-out forwards',
                'slide-up': 'slide-up 0.6s ease-out forwards',
            },
        },
    },
    plugins: [],
}
```

**Step 2: Replace input.css font imports and base styles**

Replace the top of `main/static/css/input.css` up to (but not including) the existing animation classes with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Inter:wght@300;400;500;600&display=swap');

/* ===== Base ===== */
html { scroll-behavior: smooth; }

body {
    background-color: #0a0800;
    color: #fde68a;
}

/* Ambient CRT glow — dark room atmosphere */
body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: radial-gradient(ellipse 80% 50% at 50% 100%, rgba(234, 88, 12, 0.07) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ===== Scrollbar ===== */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #0a0800; }
::-webkit-scrollbar-thumb { background: #d97706; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #f59e0b; }

/* ===== Glass Card ===== */
.glass-card {
    background: rgba(245, 158, 11, 0.04);
    border: 1px solid rgba(245, 158, 11, 0.15);
    box-shadow: 0 0 20px rgba(234, 88, 12, 0.08);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

.glass-card:hover {
    border-color: rgba(245, 158, 11, 0.3);
    box-shadow: 0 0 40px rgba(234, 88, 12, 0.18);
}

/* ===== Terminal Prompt ===== */
.terminal-prompt::before {
    content: '> ';
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
}

/* ===== Section Header ===== */
.section-header {
    font-family: 'JetBrains Mono', monospace;
    color: #f59e0b;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.section-header::before { content: '> '; }

/* ===== Terminal Divider ===== */
.terminal-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    color: rgba(245, 158, 11, 0.2);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    margin: 0;
}

.terminal-divider::before,
.terminal-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(245, 158, 11, 0.15);
}

/* ===== Amber Glow Button ===== */
.btn-terminal {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.875rem;
    padding: 0.625rem 1.5rem;
    background: transparent;
    border: 1px solid rgba(245, 158, 11, 0.4);
    color: #fbbf24;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}

.btn-terminal::before {
    content: '[ ';
    color: #f59e0b;
}

.btn-terminal::after {
    content: ' ]';
    color: #f59e0b;
}

.btn-terminal:hover {
    background: rgba(245, 158, 11, 0.1);
    border-color: #f59e0b;
    box-shadow: 0 0 20px rgba(234, 88, 12, 0.3);
    color: #fde68a;
}

/* ===== Amber Solid Button ===== */
.btn-amber {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.875rem;
    padding: 0.625rem 1.5rem;
    background: #d97706;
    border: 1px solid #f59e0b;
    color: #0a0800;
    font-weight: 700;
    transition: all 0.2s ease;
}

.btn-amber:hover {
    background: #f59e0b;
    box-shadow: 0 0 30px rgba(234, 88, 12, 0.5);
}

/* ===== CRT Bezel (hero photo frame) ===== */
.crt-bezel {
    position: relative;
    border-radius: 12px;
    border: 3px solid #d97706;
    box-shadow:
        0 0 0 6px rgba(245, 158, 11, 0.08),
        0 0 40px rgba(234, 88, 12, 0.4),
        0 0 80px rgba(234, 88, 12, 0.2),
        inset 0 0 20px rgba(234, 88, 12, 0.15);
    overflow: hidden;
    animation: crt-flicker 8s infinite;
}

/* Scanlines on bezel only */
.crt-bezel::after {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 0, 0, 0.08) 2px,
        rgba(0, 0, 0, 0.08) 4px
    );
    pointer-events: none;
    z-index: 10;
}

/* ===== ASCII Progress Bar ===== */
.ascii-bar {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.875rem;
    color: #f59e0b;
    white-space: nowrap;
}

.ascii-bar-track {
    color: rgba(245, 158, 11, 0.25);
}

/* ===== Terminal Input Fields ===== */
.terminal-input {
    background: rgba(245, 158, 11, 0.04);
    border: 1px solid rgba(245, 158, 11, 0.2);
    color: #fde68a;
    font-family: 'Inter', sans-serif;
    padding: 0.75rem 1rem 0.75rem 2rem;
    transition: border-color 0.2s, box-shadow 0.2s;
    width: 100%;
}

.terminal-input:focus {
    outline: none;
    border-color: #f59e0b;
    box-shadow: 0 0 15px rgba(234, 88, 12, 0.2);
}

.terminal-input::placeholder { color: #92400e; }

.input-wrapper {
    position: relative;
}

.input-wrapper::before {
    content: '>';
    position: absolute;
    left: 0.75rem;
    top: 50%;
    transform: translateY(-50%);
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.875rem;
    pointer-events: none;
}

.input-wrapper-textarea::before {
    top: 1rem;
    transform: none;
}

/* ===== Fade-in scroll animations ===== */
.fade-in-section {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease-out, transform 0.6s ease-out;
    will-change: opacity, transform;
}

.fade-in-section.is-visible {
    opacity: 1;
    transform: none;
}

.stagger-reveal > * {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.5s ease-out, transform 0.5s ease-out;
}

.stagger-reveal.is-visible > * { opacity: 1; transform: translateY(0); }
.stagger-reveal.is-visible > *:nth-child(1) { transition-delay: 0ms; }
.stagger-reveal.is-visible > *:nth-child(2) { transition-delay: 100ms; }
.stagger-reveal.is-visible > *:nth-child(3) { transition-delay: 200ms; }
.stagger-reveal.is-visible > *:nth-child(4) { transition-delay: 300ms; }
.stagger-reveal.is-visible > *:nth-child(5) { transition-delay: 400ms; }
.stagger-reveal.is-visible > *:nth-child(6) { transition-delay: 500ms; }
.stagger-reveal.is-visible > *:nth-child(7) { transition-delay: 600ms; }
.stagger-reveal.is-visible > *:nth-child(8) { transition-delay: 700ms; }
.stagger-reveal.is-visible > *:nth-child(9) { transition-delay: 800ms; }

/* ===== Timeline ===== */
.timeline-line.is-visible { animation: draw-line 1.5s ease-out forwards; }

/* ===== Mobile menu ===== */
.mobile-menu-enter { display: none; }
.mobile-menu-enter.open { display: block; }

/* ===== Custom scrollbar for containers ===== */
.custom-scrollbar { scrollbar-width: thin; scrollbar-color: #d97706 rgba(10,8,0,0.3); }
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: rgba(10,8,0,0.3); border-radius: 8px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #d97706; border-radius: 8px; }

/* ===== Toast messages ===== */
.toast-message { transform: translateX(100%); opacity: 0; }

/* ===== Bento grid ===== */
.bento-featured { grid-column: span 2; }
@media (max-width: 768px) { .bento-featured { grid-column: span 1; } }

/* ===== Terminal tag badge ===== */
.tag-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #d97706;
    border: 1px solid rgba(217, 119, 6, 0.4);
    padding: 0.1rem 0.4rem;
    border-radius: 2px;
    background: rgba(245, 158, 11, 0.06);
}

.tag-badge::before { content: '['; }
.tag-badge::after { content: ']'; }

/* ===== Testimonial marquee ===== */
.marquee-track {
    display: flex;
    gap: 1.5rem;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    -ms-overflow-style: none;
    scrollbar-width: none;
    padding-bottom: 0.5rem;
}

.marquee-track::-webkit-scrollbar { display: none; }
.marquee-track > * { scroll-snap-align: start; flex-shrink: 0; }

/* ===== Scroll progress bar ===== */
#scroll-progress {
    background: linear-gradient(to right, #d97706, #f59e0b, #ea580c);
}
```

**Step 3: Build CSS**

```bash
cd /home/sraldon/Projects/portfolio1 && npm run build:css
```
Expected: `output.css` rebuilt with no errors.

**Step 4: Commit**

```bash
git add tailwind.config.js main/static/css/input.css
git commit -m "feat: add amber CRT design tokens and base CSS"
```

---

## Task 2: base.html — Navigation + Footer

**Files:**
- Modify: `main/templates/main/base.html`

**Step 1: Replace the entire base.html**

Replace `main/templates/main/base.html` with the following. **Keep all Django template tags exactly as-is.**

```html
{% load i18n static %}
<!doctype html>
<html lang="{{ LANGUAGE_CODE }}">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}{% trans "Portfolio" %}{% endblock %}</title>
    <meta name="description" content="{% trans 'Professional Portfolio displaying projects, skills, and experience.' %}" />
    <meta name="author" content="Amir Sraldon" />
    <meta property="og:title" content="{% trans 'Portfolio' %} - Amir Sraldon" />
    <meta property="og:description" content="{% trans 'Professional Portfolio displaying projects, skills, and experience.' %}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{{ request.build_absolute_uri }}" />
    <meta property="twitter:card" content="summary_large_image" />
    <link rel="icon" type="image/x-icon" href="{% static 'favicon.ico' %}">
    <link rel="stylesheet" href="{% static 'css/output.css' %}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
</head>

<body class="bg-crt-bg text-crt-text font-sans antialiased">

    <!-- Scroll Progress Bar -->
    <div id="scroll-progress" class="fixed top-0 left-0 h-0.5 z-[60]" style="width: 0%;"></div>

    <!-- Navigation -->
    <nav id="main-nav" class="fixed w-full z-50 border-b border-crt-amber/20 transition-all duration-300 bg-crt-bg/80 backdrop-blur-sm">
        <div class="container mx-auto px-6 py-4 flex justify-between items-center">

            <!-- Logo -->
            <a href="{% url 'home' %}" class="font-mono text-crt-amber font-bold text-lg tracking-wider hover:text-crt-amber-light transition-colors">
                {% if profile %}{{ profile.name }}{% else %}Portfolio{% endif %}<span class="animate-blink text-crt-glow">_</span>
            </a>

            <div class="flex items-center gap-6">
                <!-- Desktop Nav -->
                <div class="hidden md:flex items-center gap-6">
                    <a href="#system-info" class="nav-link font-mono text-sm text-crt-muted hover:text-crt-amber transition-colors">{% trans "About" %}</a>
                    <a href="#projects" class="nav-link font-mono text-sm text-crt-muted hover:text-crt-amber transition-colors">{% trans "Projects" %}</a>
                    <a href="#career" class="nav-link font-mono text-sm text-crt-muted hover:text-crt-amber transition-colors">{% trans "Career" %}</a>
                    <a href="#contact" class="nav-link font-mono text-sm text-crt-muted hover:text-crt-amber transition-colors">{% trans "Contact" %}</a>
                </div>

                <!-- Language Switcher -->
                <div class="flex items-center gap-1 font-mono text-sm">
                    {% get_current_language as LANGUAGE_CODE %}
                    {% get_available_languages as LANGUAGES %}
                    {% get_language_info_list for LANGUAGES as languages %}
                    {% for language in languages %}
                    <a href="/{{ language.code }}/"
                        class="px-2 py-1 border transition-colors {% if language.code == LANGUAGE_CODE %}border-crt-amber text-crt-amber bg-crt-amber/10{% else %}border-crt-muted/30 text-crt-muted hover:border-crt-amber hover:text-crt-amber{% endif %}">
                        {{ language.code|upper }}
                    </a>
                    {% endfor %}
                </div>
            </div>

            <!-- Mobile hamburger -->
            <button id="mobile-menu-btn" class="md:hidden text-crt-amber hover:text-crt-amber-light focus:outline-none">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path>
                </svg>
            </button>
        </div>

        <!-- Mobile Menu -->
        <div id="mobile-menu" class="mobile-menu-enter md:hidden bg-crt-bg/98 backdrop-blur-md border-b border-crt-amber/20 absolute w-full left-0 top-full shadow-xl z-40">
            <div class="flex flex-col p-6 gap-4">
                <a href="#system-info" class="mobile-link font-mono text-crt-text hover:text-crt-amber transition-colors py-2 border-b border-crt-amber/10">{% trans "About" %}</a>
                <a href="#projects" class="mobile-link font-mono text-crt-text hover:text-crt-amber transition-colors py-2 border-b border-crt-amber/10">{% trans "Projects" %}</a>
                <a href="#career" class="mobile-link font-mono text-crt-text hover:text-crt-amber transition-colors py-2 border-b border-crt-amber/10">{% trans "Career" %}</a>
                <a href="#contact" class="mobile-link font-mono text-crt-text hover:text-crt-amber transition-colors py-2">{% trans "Contact" %}</a>
            </div>
        </div>
    </nav>

    <main class="pt-16 relative z-10">
        {% if messages %}
        <div id="toast-container" class="fixed bottom-5 right-5 z-50 flex flex-col gap-3">
            {% for message in messages %}
            <div class="toast-message transition-all duration-500 flex items-center w-full max-w-xs p-4 glass-card text-crt-text mb-2" role="alert">
                {% if message.tags == 'success' %}
                <i class="fa-solid fa-circle-check text-green-400 mr-3"></i>
                {% elif message.tags == 'error' %}
                <i class="fa-solid fa-circle-xmark text-red-400 mr-3"></i>
                {% else %}
                <i class="fa-solid fa-circle-info text-crt-amber mr-3"></i>
                {% endif %}
                <div class="text-sm font-sans">{{ message }}</div>
                <button class="ml-auto text-crt-muted hover:text-crt-text" onclick="this.parentElement.remove()">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 14 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                    </svg>
                </button>
            </div>
            {% endfor %}
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', () => {
                document.querySelectorAll('.toast-message').forEach((t, i) => {
                    setTimeout(() => t.classList.remove('translate-x-full', 'opacity-0'), 100 * i);
                    setTimeout(() => { t.style.opacity = '0'; setTimeout(() => t.remove(), 500); }, 5000 + 100 * i);
                });
            });
        </script>
        {% endif %}

        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-crt-bg border-t border-crt-amber/15 py-8 mt-20 fade-in-section">
        <div class="container mx-auto px-6 text-center">
            <p class="font-mono text-sm text-crt-muted">
                <span class="text-crt-amber">©</span> {% now "Y" %} {% if profile %}{{ profile.name }}{% endif %} <span class="text-crt-amber/40">—</span> {% trans "All rights reserved." %}
            </p>
        </div>
    </footer>

    <!-- Global Scripts -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            // Mobile menu
            const menuBtn = document.getElementById('mobile-menu-btn');
            const mobileMenu = document.getElementById('mobile-menu');
            if (menuBtn && mobileMenu) {
                menuBtn.addEventListener('click', () => mobileMenu.classList.toggle('open'));
                mobileMenu.querySelectorAll('.mobile-link').forEach(l => l.addEventListener('click', () => mobileMenu.classList.remove('open')));
            }

            // Scroll progress
            const scrollProgress = document.getElementById('scroll-progress');
            const mainNav = document.getElementById('main-nav');

            window.addEventListener('scroll', () => {
                const scrollTop = window.scrollY;
                const docHeight = document.documentElement.scrollHeight - window.innerHeight;
                if (scrollProgress) scrollProgress.style.width = (docHeight > 0 ? (scrollTop / docHeight) * 100 : 0) + '%';
                if (mainNav) {
                    mainNav.classList.toggle('bg-crt-bg/95', scrollTop > 50);
                    mainNav.classList.toggle('shadow-lg', scrollTop > 50);
                    mainNav.classList.toggle('bg-crt-bg/80', scrollTop <= 50);
                }
            }, { passive: true });

            // Active nav highlight
            const navLinks = document.querySelectorAll('.nav-link');
            const sections = document.querySelectorAll('section[id]');
            const sectionObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const id = entry.target.getAttribute('id');
                        navLinks.forEach(link => {
                            const active = link.getAttribute('href') === '#' + id;
                            link.classList.toggle('text-crt-amber', active);
                            link.classList.toggle('text-crt-muted', !active);
                        });
                    }
                });
            }, { rootMargin: '-20% 0px -60% 0px', threshold: 0 });
            sections.forEach(s => sectionObserver.observe(s));

            // Fade-in observer
            const revealObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        revealObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });
            document.querySelectorAll('.fade-in-section, .stagger-reveal, .timeline-line').forEach(el => revealObserver.observe(el));
        });
    </script>
</body>
</html>
```

**Step 2: Build CSS and verify nav renders**

```bash
npm run build:css
python manage.py runserver
```
Open browser → check nav has amber accent, monospace font, dark background.

**Step 3: Commit**

```bash
git add main/templates/main/base.html
git commit -m "feat: amber CRT nav and footer in base.html"
```

---

## Task 3: Zone 1 — BOOT Hero Section

**Files:**
- Modify: `main/templates/main/home.html` (replace entire file, build zone by zone)

**Step 1: Start fresh home.html — Zone 1 only**

Replace `main/templates/main/home.html` with just the hero zone first:

```html
{% extends 'main/base.html' %}
{% load i18n %}
{% block content %}

<!-- ═══════════════════════════════════════════
     ZONE 1 — BOOT (Hero)
     ═══════════════════════════════════════════ -->
<section id="about" class="min-h-screen flex items-center justify-center relative overflow-hidden pt-16">

    <!-- Background: hero bg options (video/image/slideshow) — unchanged logic -->
    <div class="absolute inset-0 z-0">
        {% if profile.hero_bg_type == 'VIDEO' and profile.hero_video_file %}
        <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover">
            <source src="{{ profile.hero_video_file.url }}" type="video/mp4">
        </video>
        <div class="absolute inset-0 bg-crt-bg" style="opacity: {{ profile.hero_overlay_opacity }};"></div>
        {% elif profile.hero_bg_type == 'IMAGE' and profile.hero_static_image %}
        <div class="absolute inset-0 w-full h-full bg-cover bg-center bg-no-repeat"
            style="background-image: url('{{ profile.hero_static_image.url }}');"></div>
        <div class="absolute inset-0 bg-crt-bg" style="opacity: {{ profile.hero_overlay_opacity }};"></div>
        {% elif profile.hero_bg_type == 'SLIDESHOW' %}
        <div class="slideshow-container absolute inset-0 w-full h-full">
            {% for slide in profile.hero_slides.all %}
            <div class="slide absolute inset-0 w-full h-full bg-cover bg-center bg-no-repeat transition-opacity duration-1000 {% if not forloop.first %}opacity-0{% endif %}"
                style="background-image: url('{{ slide.image.url }}');"></div>
            {% endfor %}
        </div>
        <div class="absolute inset-0 bg-crt-bg" style="opacity: {{ profile.hero_overlay_opacity }};"></div>
        {% else %}
        <!-- Default: bottom amber glow (handled by body::before in CSS) -->
        {% endif %}
    </div>

    <!-- Hero content: split layout -->
    <div class="container mx-auto px-6 z-10 relative">
        <div class="flex flex-col lg:flex-row items-center justify-between gap-12 lg:gap-20">

            <!-- Left: Terminal boot sequence -->
            <div class="flex-1 max-w-xl">
                <!-- Boot sequence terminal card -->
                <div class="glass-card rounded-lg p-6 mb-8 font-mono text-sm" id="boot-terminal">
                    <div class="flex items-center gap-2 mb-4 pb-3 border-b border-crt-amber/20">
                        <span class="w-3 h-3 rounded-full bg-red-500/60"></span>
                        <span class="w-3 h-3 rounded-full bg-yellow-500/60"></span>
                        <span class="w-3 h-3 rounded-full bg-green-500/60"></span>
                        <span class="ml-2 text-crt-muted text-xs">portfolio.sh</span>
                    </div>
                    <div id="boot-lines" class="space-y-1 text-crt-text">
                        <!-- Lines injected by JS -->
                    </div>
                    <span class="animate-blink text-crt-amber">█</span>
                </div>

                <!-- Name — large, after boot -->
                <h1 id="hero-name" class="text-4xl md:text-6xl font-mono font-bold text-crt-amber mb-4 opacity-0 transition-all duration-700 translate-y-4">
                    {{ profile.name }}
                </h1>

                <!-- Bio -->
                <p id="hero-bio" class="text-crt-text/80 font-sans text-lg leading-relaxed mb-8 opacity-0 transition-all duration-700 translate-y-4 delay-200 max-w-lg">
                    {{ profile.bio|default:"" }}
                </p>

                <!-- CTA buttons -->
                <div id="hero-ctas" class="flex flex-wrap gap-4 opacity-0 transition-all duration-700 translate-y-4">
                    {% if profile.resume %}
                    <a href="{{ profile.resume.url }}" download class="btn-amber rounded-sm">
                        ./resume.pdf
                    </a>
                    {% endif %}
                    <a href="#contact" class="btn-terminal rounded-sm">
                        ./contact
                    </a>
                </div>
            </div>

            <!-- Right: CRT bezel photo -->
            <div class="flex-shrink-0">
                <div class="crt-bezel w-64 h-64 md:w-80 md:h-80">
                    {% if profile.profile_picture %}
                    <img src="{{ profile.profile_picture.url }}" alt="{{ profile.name }}"
                        class="w-full h-full object-cover">
                    {% else %}
                    <div class="w-full h-full bg-crt-surface flex items-center justify-center">
                        <i class="fa-solid fa-user text-6xl text-crt-amber/40"></i>
                    </div>
                    {% endif %}
                </div>
                <!-- Glow floor under the monitor -->
                <div class="w-full h-4 mt-2 bg-crt-glow/20 blur-xl rounded-full mx-auto" style="max-width: 280px;"></div>
            </div>
        </div>
    </div>
</section>

<!-- Terminal divider -->
<div class="terminal-divider my-0 px-6">// </div>

{% endblock %}
```

**Step 2: Add boot sequence JS at bottom of home.html (before `{% endblock %}`)**

Add this script just before `{% endblock %}`:

```html
<script>
document.addEventListener('DOMContentLoaded', () => {
    // Boot sequence
    const bootLines = [
        { text: 'Initializing portfolio...', delay: 300 },
        { text: 'Loading profile data... OK', delay: 700 },
        { text: 'Name: {{ profile.name }}', delay: 1100 },
        { text: 'Status: Available for work', delay: 1500 },
        { text: 'Languages: EN / FR', delay: 1900 },
        { text: 'Portfolio ready.', delay: 2300 },
    ];

    const container = document.getElementById('boot-lines');
    const name = document.getElementById('hero-name');
    const bio = document.getElementById('hero-bio');
    const ctas = document.getElementById('hero-ctas');

    bootLines.forEach(({ text, delay }) => {
        setTimeout(() => {
            const line = document.createElement('p');
            line.innerHTML = `<span class="text-crt-amber">></span> <span class="text-crt-text">${text}</span>`;
            container.appendChild(line);
        }, delay);
    });

    // Reveal name, bio, CTAs after boot
    setTimeout(() => {
        [name, bio, ctas].forEach((el, i) => {
            if (el) {
                setTimeout(() => {
                    el.classList.remove('opacity-0', 'translate-y-4');
                }, i * 150);
            }
        });
    }, 2600);

    // Slideshow logic (unchanged)
    const slides = document.querySelectorAll('.slide');
    if (slides.length > 1) {
        let currentSlide = 0;
        setInterval(() => {
            slides[currentSlide].classList.add('opacity-0');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.remove('opacity-0');
        }, 5000);
    }
});
</script>
```

**Step 3: Build CSS, run server, check hero**

```bash
npm run build:css && python manage.py runserver
```
Verify: terminal boot sequence types out, name fades in, CRT bezel photo glows.

**Step 4: Commit**

```bash
git add main/templates/main/home.html main/static/css/input.css
git commit -m "feat: Zone 1 BOOT hero with CRT bezel and terminal boot sequence"
```

---

## Task 4: Zone 2 — SYSTEM INFO (Bio + Skills)

**Files:**
- Modify: `main/templates/main/home.html` (append new zone before `{% endblock %}`)

**Step 1: Append Zone 2 to home.html before `{% endblock %}`**

Add after the Zone 1 divider:

```html
<!-- ═══════════════════════════════════════════
     ZONE 2 — SYSTEM INFO (Bio + Skills)
     ═══════════════════════════════════════════ -->
<section id="system-info" class="py-24 fade-in-section">
    <div class="container mx-auto px-6">
        <p class="section-header">system.info</p>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">

            <!-- Bio card -->
            <div class="glass-card rounded-lg p-6">
                <div class="flex items-center gap-2 mb-4 pb-3 border-b border-crt-amber/20 font-mono text-xs text-crt-muted">
                    <i class="fa-solid fa-circle-user text-crt-amber"></i>
                    about.txt
                </div>
                <p class="font-sans text-crt-text leading-relaxed">{{ profile.bio|default:"" }}</p>

                <!-- Contact info links -->
                <div class="mt-6 space-y-2 font-mono text-sm">
                    {% if contact_info.email %}
                    <p class="text-crt-muted"><span class="text-crt-amber">></span> email: <span class="text-crt-text">{{ contact_info.email }}</span></p>
                    {% endif %}
                    {% if contact_info.github_url %}
                    <p class="text-crt-muted"><span class="text-crt-amber">></span> github: <a href="{{ contact_info.github_url }}" target="_blank" class="text-crt-amber-light hover:text-crt-amber transition-colors">{{ contact_info.github_url|cut:"https://github.com/" }}</a></p>
                    {% endif %}
                    {% if contact_info.linkedin_url %}
                    <p class="text-crt-muted"><span class="text-crt-amber">></span> linkedin: <a href="{{ contact_info.linkedin_url }}" target="_blank" class="text-crt-amber-light hover:text-crt-amber transition-colors">linked.in/...</a></p>
                    {% endif %}
                </div>
            </div>

            <!-- Skills terminal card -->
            <div class="glass-card rounded-lg p-6" id="skills-card">
                <div class="flex items-center gap-2 mb-4 pb-3 border-b border-crt-amber/20 font-mono text-xs text-crt-muted">
                    <i class="fa-solid fa-microchip text-crt-amber"></i>
                    skills.log
                </div>
                <div class="space-y-3 max-h-80 overflow-y-auto custom-scrollbar pr-2" id="skills-section">
                    {% for skill in skills %}
                    <div class="skill-row font-mono text-sm">
                        <div class="flex justify-between items-center mb-1">
                            <span class="text-crt-text">{{ skill.name }}</span>
                            <span class="text-crt-amber skill-counter text-xs" data-target="{{ skill.proficiency }}">0%</span>
                        </div>
                        <div class="ascii-bar text-xs" data-width="{{ skill.proficiency|default:0 }}">
                            <span class="ascii-bar-track">░░░░░░░░░░░░░░░░░░░░</span>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</section>

<div class="terminal-divider my-0 px-6">// </div>
```

**Step 2: Add ASCII skill bar JS to the script block**

In the existing `<script>` block (at bottom of home.html), add inside `DOMContentLoaded`:

```js
// ASCII skill bars
const skillsSection = document.getElementById('skills-section');
if (skillsSection) {
    const skillObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.querySelectorAll('.skill-row').forEach(row => {
                const bar = row.querySelector('.ascii-bar');
                const counter = row.querySelector('.skill-counter');
                const width = parseInt(bar.dataset.width, 10);
                const total = 20;
                const filled = Math.round((width / 100) * total);
                bar.innerHTML = `<span class="text-crt-amber">${'█'.repeat(filled)}</span><span class="ascii-bar-track">${'░'.repeat(total - filled)}</span>`;
                // Counter animation
                let current = 0;
                const step = Math.ceil(width / 40);
                const interval = setInterval(() => {
                    current = Math.min(current + step, width);
                    counter.textContent = current + '%';
                    if (current >= width) clearInterval(interval);
                }, 30);
            });
            skillObserver.unobserve(entry.target);
        });
    }, { threshold: 0.2 });
    skillObserver.observe(skillsSection);
}
```

**Step 3: Build and verify**

```bash
npm run build:css && python manage.py runserver
```
Scroll to skills — verify ASCII bars animate in.

**Step 4: Commit**

```bash
git add main/templates/main/home.html
git commit -m "feat: Zone 2 SYSTEM INFO with bio and ASCII skill bars"
```

---

## Task 5: Zone 3 — PROJECTS Bento Grid

**Files:**
- Modify: `main/templates/main/home.html`

**Step 1: Append Zone 3**

```html
<!-- ═══════════════════════════════════════════
     ZONE 3 — PROJECTS
     ═══════════════════════════════════════════ -->
<section id="projects" class="py-24 fade-in-section">
    <div class="container mx-auto px-6">
        <p class="section-header">projects.list</p>
        <h2 class="text-3xl md:text-4xl font-mono font-bold text-crt-amber mb-12">
            {% trans "Featured Projects" %}
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 stagger-reveal">
            {% for project in projects %}
            <div class="glass-card rounded-lg overflow-hidden group transition-all hover:-translate-y-1 {% if forloop.first %}bento-featured{% endif %}">
                <!-- Image -->
                <div class="h-44 overflow-hidden relative">
                    {% if project.image %}
                    <img src="{{ project.image.url }}" alt="{{ project.title }}"
                        class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500">
                    {% else %}
                    <div class="w-full h-full bg-crt-surface flex items-center justify-center">
                        <i class="fa-solid fa-code text-3xl text-crt-amber/30"></i>
                    </div>
                    {% endif %}
                    <!-- Amber overlay on hover -->
                    <div class="absolute inset-0 bg-gradient-to-t from-crt-bg via-transparent to-transparent opacity-60"></div>
                    <div class="absolute inset-0 bg-crt-amber/0 group-hover:bg-crt-amber/10 transition-colors duration-300"></div>
                </div>

                <!-- Content -->
                <div class="p-5">
                    <div class="flex justify-between items-start mb-3">
                        <h3 class="font-mono font-bold text-crt-text text-lg">{{ project.title }}</h3>
                        <span class="font-mono text-xs text-crt-muted">[{{ project.created_date|date:"Y" }}]</span>
                    </div>
                    {% if project.description %}
                    <p class="font-sans text-crt-text/70 text-sm mb-4 line-clamp-3">{{ project.description }}</p>
                    {% endif %}
                    <div class="flex gap-3">
                        {% if project.code_link %}
                        <a href="{{ project.code_link }}" target="_blank"
                            class="flex-1 text-center py-1.5 font-mono text-xs border border-crt-amber/30 text-crt-muted hover:border-crt-amber hover:text-crt-amber transition-colors">
                            [{% trans "code" %}]
                        </a>
                        {% endif %}
                        {% if project.demo_link %}
                        <a href="{{ project.demo_link }}" target="_blank"
                            class="flex-1 text-center py-1.5 font-mono text-xs bg-crt-amber/10 border border-crt-amber/40 text-crt-amber hover:bg-crt-amber/20 transition-colors">
                            [{% trans "demo" %}]
                        </a>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<div class="terminal-divider my-0 px-6">// </div>
```

**Step 2: Build and verify bento grid**

```bash
npm run build:css && python manage.py runserver
```
Verify first project card is wider (bento-featured), amber hover glow works.

**Step 3: Commit**

```bash
git add main/templates/main/home.html
git commit -m "feat: Zone 3 PROJECTS bento grid with amber glass cards"
```

---

## Task 6: Zone 4 — CAREER Timeline (Experience + Education merged)

**Files:**
- Modify: `main/templates/main/home.html`

**Step 1: Append Zone 4**

```html
<!-- ═══════════════════════════════════════════
     ZONE 4 — CAREER (Experience + Education)
     ═══════════════════════════════════════════ -->
<section id="career" class="py-24 bg-crt-surface/30 fade-in-section">
    <div class="container mx-auto px-6">
        <p class="section-header">career.log</p>
        <h2 class="text-3xl md:text-4xl font-mono font-bold text-crt-amber mb-12">
            {% trans "Experience" %} <span class="text-crt-muted">&</span> {% trans "Education" %}
        </h2>

        <!-- Unified timeline -->
        <div class="relative max-w-3xl mx-auto">
            <!-- Center line -->
            <div class="absolute left-1/2 top-0 bottom-0 w-px bg-gradient-to-b from-crt-amber/60 via-crt-amber/30 to-transparent -translate-x-1/2 timeline-line"></div>

            <div class="space-y-10">

                <!-- Experience entries -->
                {% for exp in experiences %}
                <div class="relative flex {% if forloop.counter|divisibleby:2 %}flex-row-reverse{% else %}flex-row{% endif %} items-start gap-8 fade-in-section">
                    <!-- Dot -->
                    <div class="absolute left-1/2 top-1 -translate-x-1/2 w-4 h-4 rounded-full border-2 border-crt-amber bg-crt-bg flex items-center justify-center z-10">
                        <span class="text-crt-amber text-xs">●</span>
                    </div>
                    <!-- Card -->
                    <div class="w-5/12 {% if forloop.counter|divisibleby:2 %}mr-auto pr-4{% else %}ml-auto pl-4{% endif %}">
                        <div class="glass-card rounded-lg p-4">
                            <p class="font-mono text-xs text-crt-muted mb-1">
                                [{{ exp.start_date|date:"Y-m" }}] → [{% if exp.end_date %}{{ exp.end_date|date:"Y-m" }}{% else %}present{% endif %}]
                            </p>
                            <h3 class="font-mono font-bold text-crt-text mb-0.5">{{ exp.job_title }}</h3>
                            <p class="font-mono text-sm text-crt-amber mb-2">{{ exp.company }}</p>
                            {% if exp.description %}
                            <p class="font-sans text-sm text-crt-text/70">{{ exp.description }}</p>
                            {% endif %}
                        </div>
                    </div>
                    <div class="w-5/12"></div>
                </div>
                {% endfor %}

                <!-- Education entries -->
                {% for edu in educations %}
                <div class="relative flex {% if forloop.counter|divisibleby:2 %}flex-row{% else %}flex-row-reverse{% endif %} items-start gap-8 fade-in-section">
                    <!-- Dot (diamond shape via rotation) -->
                    <div class="absolute left-1/2 top-1 -translate-x-1/2 w-4 h-4 border-2 border-crt-amber-light bg-crt-bg rotate-45 z-10"></div>
                    <!-- Card -->
                    <div class="w-5/12 {% if forloop.counter|divisibleby:2 %}ml-auto pl-4{% else %}mr-auto pr-4{% endif %}">
                        <div class="glass-card rounded-lg p-4 border-crt-amber-light/20">
                            <p class="font-mono text-xs text-crt-muted mb-1">
                                [{{ edu.start_date|date:"Y" }}] → [{% if edu.end_date %}{{ edu.end_date|date:"Y" }}{% else %}present{% endif %}]
                            </p>
                            <h3 class="font-mono font-bold text-crt-text mb-0.5">{{ edu.degree }}</h3>
                            <p class="font-mono text-sm text-crt-amber-light">{{ edu.institution }}</p>
                        </div>
                    </div>
                    <div class="w-5/12"></div>
                </div>
                {% endfor %}

            </div>
        </div>
    </div>
</section>

<div class="terminal-divider my-0 px-6">// </div>
```

**Step 2: Build and verify**

```bash
npm run build:css && python manage.py runserver
```
Verify alternating left/right timeline, amber line, experience (●) vs education (◆) dots.

**Step 3: Commit**

```bash
git add main/templates/main/home.html
git commit -m "feat: Zone 4 CAREER unified timeline merging experience and education"
```

---

## Task 7: Zone 5 — HUMAN (Hobbies)

**Files:**
- Modify: `main/templates/main/home.html`

**Step 1: Append Zone 5**

```html
<!-- ═══════════════════════════════════════════
     ZONE 5 — HUMAN (Hobbies)
     ═══════════════════════════════════════════ -->
<section id="hobbies" class="py-24 fade-in-section">
    <div class="container mx-auto px-6">
        <p class="section-header">human.exe</p>
        <p class="font-mono text-xs text-crt-muted mb-8">// not just a developer</p>
        <h2 class="text-3xl md:text-4xl font-mono font-bold text-crt-amber mb-12">
            {% trans "My Hobbies" %}
        </h2>

        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 stagger-reveal">
            {% for hobby in hobbies %}
            <div class="glass-card rounded-lg p-5 text-center group hover:-translate-y-1 transition-all duration-300">
                <div class="w-12 h-12 mx-auto mb-3 rounded-full bg-crt-amber/5 border border-crt-amber/20 flex items-center justify-center group-hover:bg-crt-amber/15 group-hover:border-crt-amber/40 transition-all">
                    {% if hobby.font_awesome_icon %}
                    <i class="{{ hobby.font_awesome_icon }} text-xl text-crt-amber group-hover:text-crt-amber-light transition-colors"></i>
                    {% elif hobby.icon %}
                    <img src="{{ hobby.icon.url }}" alt="{{ hobby.name }}" class="w-7 h-7 object-contain" />
                    {% else %}
                    <i class="fa-solid fa-heart text-xl text-crt-amber"></i>
                    {% endif %}
                </div>
                <h3 class="font-mono text-xs font-bold text-crt-text">{{ hobby.name }}</h3>
                {% if hobby.description %}
                <p class="font-sans text-xs text-crt-muted mt-1">{{ hobby.description }}</p>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<div class="terminal-divider my-0 px-6">// </div>
```

**Step 2: Build and verify**

```bash
npm run build:css && python manage.py runserver
```

**Step 3: Commit**

```bash
git add main/templates/main/home.html
git commit -m "feat: Zone 5 HUMAN hobbies with amber glass cards"
```

---

## Task 8: Zone 6 — SOCIAL PROOF (Testimonials + Submission)

**Files:**
- Modify: `main/templates/main/home.html`

**Step 1: Append Zone 6**

```html
<!-- ═══════════════════════════════════════════
     ZONE 6 — SOCIAL PROOF (Testimonials)
     ═══════════════════════════════════════════ -->
{% if testimonials %}
<section class="py-24 bg-crt-surface/30 fade-in-section">
    <div class="container mx-auto px-6">
        <p class="section-header">reviews.log</p>
        <h2 class="text-3xl md:text-4xl font-mono font-bold text-crt-amber mb-12">
            {% trans "Testimonials" %}
        </h2>

        <!-- Horizontal scroll testimonials -->
        <div class="marquee-track pb-4">
            {% for testimonial in testimonials %}
            <div class="glass-card rounded-lg p-6 w-80 flex-shrink-0 relative">
                <div class="text-4xl text-crt-amber/30 font-mono absolute top-3 left-4">"</div>
                <p class="font-sans text-crt-text/80 text-sm italic mb-4 mt-4 relative z-10">{{ testimonial.quote }}</p>
                <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-gradient-to-br from-crt-amber to-crt-glow flex items-center justify-center font-mono font-bold text-crt-bg text-sm">
                        {{ testimonial.name|slice:":1" }}
                    </div>
                    <div>
                        <p class="font-mono text-xs font-bold text-crt-text">{{ testimonial.name }}</p>
                        {% if testimonial.role_company %}
                        <p class="font-mono text-xs text-crt-muted">{{ testimonial.role_company }}</p>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endif %}

<!-- Testimonial submission (always shown, collapsed) -->
<section class="py-12 fade-in-section">
    <div class="container mx-auto px-6 max-w-2xl">
        <!-- Toggle button -->
        <button id="toggle-testimonial-form" class="btn-terminal rounded-sm w-full font-mono text-sm mb-0">
            leave_testimonial()
        </button>

        <!-- Collapsible form -->
        <div id="testimonial-form-container" class="hidden mt-4">
            <form method="post" class="glass-card rounded-lg p-6 space-y-4">
                {% csrf_token %}
                <div class="hidden">
                    <input type="text" name="testimonial-nickname" id="testimonial-nickname">
                </div>
                {% if testimonial_form.non_field_errors %}
                <div class="p-3 bg-red-900/30 border border-red-700/50 rounded font-mono text-xs text-red-300">
                    {{ testimonial_form.non_field_errors }}
                </div>
                {% endif %}

                <div class="input-wrapper">
                    <input type="text" name="testimonial-name" required placeholder="{% trans 'Your Name' %}"
                        class="terminal-input rounded-sm" />
                </div>
                <div class="input-wrapper">
                    <input type="text" name="testimonial-role_company" placeholder="{% trans 'Role / Company (Optional)' %}"
                        class="terminal-input rounded-sm" />
                </div>
                <div class="input-wrapper input-wrapper-textarea">
                    <textarea name="testimonial-quote" required rows="3" placeholder="{% trans 'Your Testimonial' %}"
                        class="terminal-input rounded-sm pt-3"></textarea>
                </div>

                <button type="submit" name="submit_testimonial"
                    class="btn-amber w-full rounded-sm">
                    submit_testimonial()
                </button>
                <p class="font-mono text-xs text-center text-crt-muted">
                    // {% trans "Submissions are reviewed before being published." %}
                </p>
            </form>
        </div>
    </div>
</section>

<div class="terminal-divider my-0 px-6">// </div>
```

**Step 2: Add testimonial form toggle JS to the script block**

```js
// Testimonial form toggle
const toggleBtn = document.getElementById('toggle-testimonial-form');
const formContainer = document.getElementById('testimonial-form-container');
if (toggleBtn && formContainer) {
    toggleBtn.addEventListener('click', () => {
        formContainer.classList.toggle('hidden');
    });
}
```

**Step 3: Build and verify**

```bash
npm run build:css && python manage.py runserver
```
Verify testimonials scroll horizontally, form toggles open/close.

**Step 4: Commit**

```bash
git add main/templates/main/home.html
git commit -m "feat: Zone 6 SOCIAL PROOF testimonials with collapsible submission form"
```

---

## Task 9: Zone 7 — CONTACT

**Files:**
- Modify: `main/templates/main/home.html`

**Step 1: Append Zone 7**

```html
<!-- ═══════════════════════════════════════════
     ZONE 7 — CONTACT
     ═══════════════════════════════════════════ -->
<section id="contact" class="py-24 bg-crt-surface/30 fade-in-section">
    <div class="container mx-auto px-6 max-w-4xl">
        <p class="section-header">contact.init</p>
        <h2 class="text-3xl md:text-4xl font-mono font-bold text-crt-amber mb-12">
            {% trans "Get In Touch" %}
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

            <!-- whois sidebar -->
            <div class="glass-card rounded-lg p-5 font-mono text-sm space-y-3">
                <p class="text-crt-muted text-xs mb-4 pb-2 border-b border-crt-amber/15">$ whois {% if profile %}{{ profile.name|lower|cut:" " }}{% else %}amir{% endif %}</p>
                {% if contact_info.email %}
                <p><span class="text-crt-amber">email:</span> <span class="text-crt-text text-xs break-all">{{ contact_info.email }}</span></p>
                {% endif %}
                {% if contact_info.phone %}
                <p><span class="text-crt-amber">phone:</span> <span class="text-crt-text text-xs">{{ contact_info.phone }}</span></p>
                {% endif %}
                {% if contact_info.github_url %}
                <p><span class="text-crt-amber">github:</span> <a href="{{ contact_info.github_url }}" target="_blank" class="text-crt-amber-light hover:text-crt-amber text-xs transition-colors">link</a></p>
                {% endif %}
                {% if contact_info.linkedin_url %}
                <p><span class="text-crt-amber">linkedin:</span> <a href="{{ contact_info.linkedin_url }}" target="_blank" class="text-crt-amber-light hover:text-crt-amber text-xs transition-colors">link</a></p>
                {% endif %}
                {% if contact_info.twitter_url %}
                <p><span class="text-crt-amber">twitter:</span> <a href="{{ contact_info.twitter_url }}" target="_blank" class="text-crt-amber-light hover:text-crt-amber text-xs transition-colors">link</a></p>
                {% endif %}
            </div>

            <!-- Contact form -->
            <div class="md:col-span-2 glass-card rounded-lg p-6">
                <form method="post" class="space-y-4">
                    {% csrf_token %}
                    <div class="hidden">
                        <input type="text" name="contact-nickname" id="contact-nickname">
                    </div>
                    {% if contact_form.non_field_errors %}
                    <div class="p-3 bg-red-900/30 border border-red-700/50 rounded font-mono text-xs text-red-300">
                        {{ contact_form.non_field_errors }}
                    </div>
                    {% endif %}

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="input-wrapper">
                            <input type="text" name="contact-name" required placeholder="{% trans 'Name' %}"
                                class="terminal-input rounded-sm" />
                        </div>
                        <div class="input-wrapper">
                            <input type="email" name="contact-email" required placeholder="{% trans 'Email' %}"
                                class="terminal-input rounded-sm" />
                        </div>
                    </div>
                    <div class="input-wrapper">
                        <input type="text" name="contact-subject" placeholder="{% trans 'Subject' %}"
                            class="terminal-input rounded-sm" />
                    </div>
                    <div class="input-wrapper input-wrapper-textarea">
                        <textarea name="contact-message" required rows="4" placeholder="{% trans 'Message' %}"
                            class="terminal-input rounded-sm pt-3"></textarea>
                    </div>

                    <button type="submit" name="submit_contact"
                        class="btn-amber w-full rounded-sm">
                        send_message()
                    </button>
                </form>
            </div>
        </div>
    </div>
</section>
```

**Step 2: Build, verify full page**

```bash
npm run build:css && python manage.py runserver
```
Do a full scroll-through — verify all 7 zones render correctly.

**Step 3: Commit**

```bash
git add main/templates/main/home.html
git commit -m "feat: Zone 7 CONTACT with whois sidebar and terminal form"
```

---

## Task 10: Final Polish + Responsive Check

**Files:**
- Modify: `main/static/css/input.css` (minor fixes)
- Modify: `main/templates/main/home.html` (minor fixes)

**Step 1: Mobile responsive check**

Open browser devtools → toggle mobile view (375px width). Check each zone:
- Hero: stacks vertically, CRT bezel centered
- System info: single column
- Projects: single column
- Career timeline: simplify to single-side on mobile

Add to `input.css` if timeline looks broken on mobile:
```css
@media (max-width: 768px) {
    .timeline-entry { flex-direction: column !important; }
    .timeline-entry > div { width: 100% !important; padding-left: 2rem !important; padding-right: 0 !important; margin: 0 !important; }
}
```

**Step 2: Cross-browser test**

- Chrome: verify backdrop-filter blur works
- Firefox: verify glassmorphism (`-webkit-backdrop-filter` fallback in CSS)

**Step 3: FR language test**

Navigate to `/fr/` — verify all `{% trans %}` strings show French correctly.

**Step 4: Run Django tests to verify nothing broken**

```bash
python manage.py test main
```
Expected: all existing tests pass (no Python was touched).

**Step 5: Final build**

```bash
npm run build:css
```

**Step 6: Final commit**

```bash
git add -A
git commit -m "feat: complete amber CRT frontend redesign — all 7 zones"
```

---

## Summary

| Task | Zone | Status |
|------|------|--------|
| 1 | Tailwind config + CSS tokens | — |
| 2 | base.html nav + footer | — |
| 3 | Zone 1: BOOT hero | — |
| 4 | Zone 2: SYSTEM INFO | — |
| 5 | Zone 3: PROJECTS | — |
| 6 | Zone 4: CAREER timeline | — |
| 7 | Zone 5: HUMAN hobbies | — |
| 8 | Zone 6: SOCIAL PROOF | — |
| 9 | Zone 7: CONTACT | — |
| 10 | Polish + responsive | — |
