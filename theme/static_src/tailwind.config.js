module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
        './**/*.html',
    ],
    theme: {
        extend: {
            fontFamily: {
                cheltenham: ['"ITC Cheltenham Std"', 'serif'],
                helvetica: ['Helvetica', 'sans-serif'],
                bitter: ['Bitter', 'serif'],
                poppins: ['Poppins', 'sans-serif'],
            },
            screens: {
                'xs': '345px',  // Extra small screen
                'sm': '445px',  // Small screen
                'md': '768px',  // Medium screen
                'lg': '1024px', // Large screen
                'xl': '1280px', // Extra large screen
                '2xl': '1536px' // 2x extra large screen
            },
            spacing: {
                '30': '120px', // Custom class for 120px width
                '21.5': '86px' // Custom class for 86px height
            },
            colors: {
                lightgreen: {
                    100: '#d4f0c4',
                    200: '#9ce794',
                    300: '#67d765',
                    400: '#38c846',
                    500: '#28a934',
                    600: '#1f8326',
                    700: '#166018',
                    800: '#0d3e0b',
                    900: '#041d00'
                }
            }
        }
    },
    darkMode: 'class', // Enable dark mode with class strategy
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
};
