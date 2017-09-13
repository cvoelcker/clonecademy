import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';

import {BaseTest} from '../../base-test';

import {DashboardComponent} from './dashboard.component';

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [base.imports()],
      providers: [base.providers()],
      declarations: [base.entryComponents([DashboardComponent])]
    })
    TestBed.overrideModule(
      BrowserDynamicTestingModule, {
        set: {
          entryComponents: [base.entryComponents()]
        }
      }
    )
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
