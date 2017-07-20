// Karma configuration file, see link for more information
// https://karma-runner.github.io/0.13/config/configuration-file.html
let today = new Date();
let d = today.getDate();
let m = today.getMonth();
let y = today.getFullYear();

module.exports = function (config) {
  config.set({
    basePath: '',
    frameworks: ['jasmine', '@angular/cli'],
    plugins: [
      require('karma-phantomjs-launcher'),
      require('karma-jasmine'),
      require('karma-htmlfile-reporter'),
      require('@angular/cli/plugins/karma'),
      require('karma-verbose-reporter'),
    ],
    client:{
      clearContext: false, // leave Jasmine Spec Runner output visible in browser
      captureConsole: false
    },
    files: [
      { pattern: './node_modules/@angular/material/prebuilt-themes/indigo-pink.css', included: true, watched: true },
    ],

    reporters: ['verbose', "html"],

    htmlReporter: {
      outputFile: 'tests/' + y + '-' + m + '-' + d + '.html',

      // Optional
      pageTitle: 'Unit Tests',
      subPageTitle: 'A sample project description',
      groupSuites: true,
      useCompactStyle: true,
      useLegacyStyle: true
    },

    browsers: ['PhantomJS', ],
    singleRun: true
  });
};
