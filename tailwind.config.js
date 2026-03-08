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
        'crt-flicker': {
          '0%, 95%, 100%': { opacity: '1' },
          '96%': { opacity: '0.85' },
          '97%': { opacity: '1' },
          '98%': { opacity: '0.9' },
          '99%': { opacity: '1' },
        },
        blink: { '0%, 100%': { opacity: '1' }, '50%': { opacity: '0' } },
        'fade-up': {
          from: { opacity: '0', transform: 'translateY(20px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        'draw-line': { from: { height: '0%' }, to: { height: '100%' } },
        'amber-pulse': {
          '0%, 100%': { boxShadow: '0 0 20px rgba(234,88,12,0.3)' },
          '50%': { boxShadow: '0 0 50px rgba(234,88,12,0.6)' },
        },
        meteor: {
          '0%': { transform: 'rotate(215deg) translateX(0)', opacity: '1' },
          '70%': { opacity: '1' },
          '100%': { transform: 'rotate(215deg) translateX(-600px)', opacity: '0' },
        },
        'shine-sweep': {
          '0%': { left: '-100%' },
          '100%': { left: '200%' },
        },
        'border-beam': {
          '0%': { 'offset-distance': '0%' },
          '100%': { 'offset-distance': '100%' },
        },
      },
      animation: {
        'crt-flicker': 'crt-flicker 10s infinite',
        blink: 'blink 1s step-end infinite',
        'fade-up': 'fade-up 0.7s cubic-bezier(0.16,1,0.3,1) forwards',
        'draw-line': 'draw-line 1.5s cubic-bezier(0.16,1,0.3,1) forwards',
        'amber-pulse': 'amber-pulse 3s ease-in-out infinite',
        meteor: 'meteor 6s linear infinite',
        'shine-sweep': 'shine-sweep 0.5s ease forwards',
      },
    },
  },
  plugins: [],
}
