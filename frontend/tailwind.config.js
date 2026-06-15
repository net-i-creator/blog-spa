/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: {
          50: '#f7f7f8',
          100: '#eeeef1',
          200: '#d6d6dd',
          400: '#8a8a96',
          600: '#4a4a55',
          900: '#1a1a22',
        },
        brand: {
          50: '#eef4ff',
          100: '#dde9ff',
          500: '#5b7cff',
          600: '#4561e6',
          700: '#384ec4',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['"Source Serif 4"', 'Georgia', 'serif'],
      },
    },
  },
  plugins: [],
}
