/** @type {import('tailwindcss').Config} */

export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
  theme: {
    extend: {
      colors: {
        "nyu-purple": "#702b9d",
        logo: "#eeeeee",
      },
      spacing: {
        1024: "1024px",
      },
    },
  },
  plugins: [],
};
