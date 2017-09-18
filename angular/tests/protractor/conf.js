// conf.js
exports.config = {
  framework: 'jasmine',
  directConnect: true,
  specs: ['./specs.js'],
  capabilities: {
    'browserName': 'chrome',
    'chromeOptions': {
    }
  },
}
