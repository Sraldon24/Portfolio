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
