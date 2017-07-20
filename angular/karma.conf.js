// Karma configuration file, see link for more information
// https://karma-runner.github.io/0.13/config/configuration-file.html

module.exports = function (config) {
  config.set({
    basePath: '',
    frameworks: ['jasmine', '@angular/cli'],
    plugins: [
      require('karma-phantomjs-launcher'),
      require('karma-jasmine'),
      require('karma-jasmine-html-reporter'),
      require('karma-spec-reporter'),
      require('@angular/cli/plugins/karma')
    ],
    client:{
      clearContext: false, // leave Jasmine Spec Runner output visible in browser
      captureConsole: false
    },
    files: [
      { pattern: './src/test.ts', watched: false },
      { pattern: './node_modules/@angular/material/prebuilt-themes/indigo-pink.css', included: true, watched: true },
    ],
    angularCli: {
      environment: 'dev'
    },
    reporters: ["spec"],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: true,
    browsers: ['PhantomJS', ],
    singleRun: false
  });
};
