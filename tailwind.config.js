const path = require('path');

const pySitesPackages = path.join(__dirname, 'env/Lib/site-packages');

const projectPaths = [
  path.join(__dirname, 'server/templates/**/*.html'),  
];

let pyPackagesPaths = [];

if (pySitesPackages) {
  pyPackagesPaths = [
    path.join(pySitesPackages, './crispy_tailwind/**/*.html'),
    path.join(pySitesPackages, './crispy_tailwind/**/*.py'),
    path.join(pySitesPackages, './crispy_tailwind/**/*.js')
  ];
}

const contentPaths = [...projectPaths, ...pyPackagesPaths];

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: contentPaths,
  theme: {
    extend: {},
  },
  variants: {
    extend: {
      opacity: ['disabled'],
    }
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
};
