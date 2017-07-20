import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BaseTest } from '../../base-test';
import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';
import { ErrorMessageComponent } from '../../error-message/error-message.component';
import { LoaderComponent } from '../../loader/loader.component';


import { UserDetailComponent } from './user-detail.component';

describe('UserDetailComponent', () => {
  let component: UserDetailComponent;
  let fixture: ComponentFixture<UserDetailComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
      TestBed.configureTestingModule({
        imports: [ base.imports() ],
        providers: [base.providers()],
      declarations: [ UserDetailComponent, ErrorMessageComponent, LoaderComponent ]
    })
    TestBed.overrideModule(
      BrowserDynamicTestingModule, {
        set: {
          entryComponents: base.entryComponents()
        }
      }
    )
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UserDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
