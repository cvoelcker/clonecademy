import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';

import { BaseTest } from '../../base-test';

import { ModuleComponent } from './module.component';

describe('ModuleComponent', () => {
  let component: ModuleComponent;
  let fixture: ComponentFixture<ModuleComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
      TestBed.configureTestingModule({
        imports: [ base.imports() ],
        providers: [base.providers()],
        declarations: [ base.entryComponents([ ModuleComponent ]) ]
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
    fixture = TestBed.createComponent(ModuleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
