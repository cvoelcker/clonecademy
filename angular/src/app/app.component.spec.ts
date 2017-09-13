import {TestBed, async} from '@angular/core/testing';

import {MenuComponent} from './menu/menu.component';

import {AppComponent} from './app.component';

import {BaseTest} from './base-test';

describe('AppComponent', () => {
  const base = new BaseTest();
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        base.imports()
      ],
      providers: [base.providers()],
      declarations: [
        AppComponent,
        MenuComponent
      ],
    }).compileComponents();
  }));

  it('should create the app', async(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  }));


});
