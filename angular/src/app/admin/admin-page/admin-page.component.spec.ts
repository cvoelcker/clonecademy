import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BaseTest } from '../../base-test';
import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';
import { ErrorMessageComponent } from '../../error-message/error-message.component';
import { LoaderComponent } from '../../loader/loader.component';


import { AdminPageComponent } from './admin-page.component';

describe('AdminPageComponent', () => {
  let component: AdminPageComponent;
  let fixture: ComponentFixture<AdminPageComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
      TestBed.configureTestingModule({
        imports: [ base.imports() ],
        providers: [base.providers()],
      declarations: [ AdminPageComponent, ErrorMessageComponent, LoaderComponent ]
    })
    TestBed.overrideModule(
      BrowserDynamicTestingModule, {
        set: {
          entryComponents: [base.entryComponents(), LoaderComponent]
        }
      }
    )
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
