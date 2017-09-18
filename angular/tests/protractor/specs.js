// spec.js
describe('Login Verification', function() {
  beforeEach(function() {
    browser.get('http://localhost:4200');
  });

  it('should only login with verified credentials', function() {
    expect(browser.getTitle()).toEqual('Clonecademy');
    browser.waitForAngular();
    let elem = element.all(by.css('input'));
    expect(elem.count()).toEqual(2);
    elem.get(0).sendKeys("iliricon");
    elem.get(1).sendKeys("Apfelbaum");
    elem.get(1).sendKeys(protractor.Key.ENTER);
    expect(element(by.css(".error-msg")).isDisplayed()).toBeTruthy();
  });
  it('it should login with verified credentials', function() {
    expect(browser.getTitle()).toEqual('Clonecademy');
    browser.waitForAngular();
    let elem = element.all(by.css('input'));
    expect(elem.count()).toEqual(2);
    elem.get(0).sendKeys("admin");
    elem.get(1).sendKeys("Apfelbaum");
    elem.get(1).sendKeys(protractor.Key.ENTER);
    browser.waitForAngular();
    expect(element(by.css(".sidebar")).isDisplayed()).toBeTruthy();
    elem = element.all(by.css('.mat-tab-link'));
    elem.get(2).click().then(function() {
      var EC = protractor.ExpectedConditions;
      elem = element.all(by.css('button'));
      expect(elem.count()).toEqual(2);
      browser.wait(EC.elementToBeClickable(elem), 30000).then(function () {
                   elem.click();
      });
      let div = element(by.css('cdk-overlay-15'));
      elem = element.all(by.css('button')).get(0);
      browser.sleep(3000);
      browser.waitForAngular();
      elem.click();
      browser.waitForAngular();
    });
  });

});

describe('Admin Tests', function() {
  beforeAll(function() {
    browser.get('http://localhost:4200');
    expect(browser.getTitle()).toEqual('Clonecademy');
    browser.waitForAngular();
    let elem = element.all(by.css('input'));
    elem.get(0).sendKeys("admin");
    elem.get(1).sendKeys("Apfelbaum");
    elem.get(1).sendKeys(protractor.Key.ENTER);
    browser.waitForAngular();
    expect(element(by.css(".sidebar")).isDisplayed()).toBeTruthy();
  });
  it ('should create a new course', function() {
    element(by.css('.addCourse')).click()
  });
});
