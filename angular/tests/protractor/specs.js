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
  });

});

describe('Admin Tests', function() {
  beforeAll(function() {
    browser.get('http://localhost:4200');
    expect(browser.getTitle()).toEqual('Clonecademy');
    browser.waitForAngular();
    browser.waitForAngular();
    expect(element(by.css(".sidebar")).isDisplayed()).toBeTruthy();
  });
  it ('should create a new course', function() {
    element(by.css('.addCourse')).click();
    expect(element(by.css("form")).isDisplayed()).toBeTruthy();
    expect(element(by.css(".saveButton")).isEnabled()).toBeTruthy();
    let inputs = element.all(by.css('input'))
    inputs.get(0).sendKeys('TestCourse');
    let areas = element.all(by.css('textarea'));
    areas.get(0).sendKeys('This is a test course');
    let dropdowns = element.all(by.css('.mat-select-trigger'));
    dropdowns.get(0).click();
    browser.waitForAngular();
    element.all(by.css('md-option')).get(0).click();
    browser.waitForAngular();
    dropdowns.get(1).click();
    browser.sleep(500);
    browser.waitForAngular();
    element.all(by.css('md-option')).get(0).click();
    browser.waitForAngular();
    browser.sleep(500);
    let buttons = element.all(by.css('.mat-raised-button'))
    expect(buttons.count()).toEqual(4);
    buttons.get(1).click();
    expect(element(by.css('summary')).isDisplayed()).toBeTruthy();
    inputs = element.all(by.css('input'));
    inputs.get(1).sendKeys('This is a test module');
    areas = element.all(by.css('textarea'));
    areas.get(1).sendKeys('SOe description');
    dropdowns = element.all(by.css('.mat-select-trigger'));
    dropdowns.get(2).click();
    browser.sleep(500);
    browser.waitForAngular();
    expect(element.all(by.css('md-option')).count()).toEqual(3);
    browser.waitForAngular();
    expect(element(by.css(".saveButton")).isEnabled()).toBe(true);
    element.all(by.css('md-option')).get(0).click();
    browser.waitForAngular();
    browser.sleep(500);
  });
  it ('should display the admin area', function() {
    element.all(by.css('a')).get(0).click();
    browser.waitForAngular();
    let buttons = element.all(by.css('.mat-button'));
    expect(buttons.count()).toEqual(3);
    buttons.get(0).click();
    expect(element(by.css('md-select')).isDisplayed()).toBeTruthy();
    let dropdowns = element.all(by.css('.mat-select-trigger'));
    dropdowns.get(0).click();
    browser.waitForAngular();
    element.all(by.css('md-option')).get(0).click();
    browser.waitForAngular();
    browser.sleep(500);
    buttons = element.all(by.css('button'));
    expect(buttons.count()).toEqual(5);
    buttons.get(1).click();
    dropdowns = element.all(by.css('.mat-select-trigger'));
    dropdowns.get(0).click();
    browser.waitForAngular();
    element.all(by.css('md-option')).get(0).click();
    browser.waitForAngular();
    browser.sleep(500);
    expect(buttons.count()).toEqual(4);
  });
});

describe('Profile Area', function() {
  beforeAll(function() {
    browser.get('http://localhost:4200');
    expect(browser.getTitle()).toEqual('Clonecademy');
    browser.waitForAngular();
    browser.waitForAngular();
    expect(element(by.css(".sidebar")).isDisplayed()).toBeTruthy();
  });

  it('should display the profile area', function() {
    element.all(by.css('a')).get(2).click();
    browser.waitForAngular();
    let buttons = element.all(by.css('.mat-raised-button'));
    expect(buttons.count()).toEqual(3);
    buttons.get(1).click();
    browser.waitForAngular();
    // buttons = element.all(by.css('button'));
    // expect(buttons.count()).toEqual(7);
    browser.sleep(500);
    let images = element.all(by.css('img'))
    expect(images.count()).toEqual(6)
    buttons = element.all(by.css('.mat-button'));
    expect(buttons.count()).toEqual(5);
    buttons.get(0).click();
    buttons.get(1).click();
    buttons.get(2).click();
    buttons.get(3).click();
    buttons.get(4).click();
    browser.waitForAngular();
    let elem = element.all(by.css('input'));
    expect(elem.count()).toEqual(2);
  });
});

describe('Profile Area', function() {
  beforeAll(function() {
    browser.get('http://localhost:4200');
    expect(browser.getTitle()).toEqual('Clonecademy');
    browser.waitForAngular();
    browser.waitForAngular();
    expect(element(by.css(".sidebar")).isDisplayed()).toBeTruthy();
  });

  it('should display the profile area', function() {
    element.all(by.css('a')).get(2).click();
    browser.waitForAngular();
    let buttons = element.all(by.css('.mat-raised-button'));
    expect(buttons.count()).toEqual(3);
    buttons.get(1).click();
    browser.waitForAngular();
    // buttons = element.all(by.css('button'));
    // expect(buttons.count()).toEqual(7);
    browser.sleep(500);
    let images = element.all(by.css('img'))
    expect(images.count()).toEqual(6)
    buttons = element.all(by.css('.mat-button'));
    expect(buttons.count()).toEqual(5);
    buttons.get(0).click();
    buttons.get(1).click();
    buttons.get(2).click();
    buttons.get(3).click();
    buttons.get(4).click();
    browser.waitForAngular();
    let elem = element.all(by.css('input'));
    expect(elem.count()).toEqual(2);
  });
});
