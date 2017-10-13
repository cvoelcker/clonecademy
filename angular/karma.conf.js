// Karma configuration file, see link for more information
// https://karma-runner.github.io/0.13/config/configuration-file.html

module.exports = function (config) {
  config.set({
    basePath: '',
    frameworks: ['jasmine', '@angular/cli'],
    plugins: [
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
      // Optional
      pageTitle: 'Unit Tests',
      subPageTitle: 'A sample project description',
      groupSuites: true,
      useCompactStyle: true,
      useLegacyStyle: true
    },

    browsers: [],
    singleRun: false
  });
};
