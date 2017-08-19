import { async, ComponentFixture, TestBed } from '@angular/core/testing';


import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';

import { BaseTest } from '../../base-test';

import { InformationTextComponent } from './info-text.component';

describe('InformationText Component', () => {
  let component: InformationTextComponent;
  let fixture: ComponentFixture<InformationTextComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
      TestBed.configureTestingModule({
        imports: [ base.imports() ],
        providers: [base.providers()],
        declarations: [ base.entryComponents([InformationTextComponent]) ]
      })
      // TestBed.overrideModule(
      //   BrowserDynamicTestingModule, {
      //     set: {
      //       entryComponents: [base.entryComponents()]
      //     }
      //   }
      // )
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InformationTextComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
