import primeui from 'tailwindcss-primeui';
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  plugins: [primeui],
  theme: {
    extend: {
      animation: {
        shake: 'shake 0.4s cubic-bezier(.36,.07,.19,.97) both',
      },
      keyframes: {
        shake: {
          '10%, 90%': {
            transform: 'translate3d(-1px, 0, 0)',
          },
          '30%, 70%': {
            transform: 'translate3d(2px, 0, 0)',
          },
          '50%': {
            transform: 'translate3d(-2px, 0, 0)',
          },
        },
      },
    },
  },
};
