import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BaseTest } from '../../../base-test';

import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';

import { ErrorMessageComponent } from '../../../error-message/error-message.component';

import { LoaderComponent } from '../../../loader/loader.component';


import { AddQuestionComponent } from '../add-question/add-question.component';

import { AddModuleComponent } from './add-module.component';

describe('AddModuleComponent', () => {
  let component: AddModuleComponent;
  let fixture: ComponentFixture<AddModuleComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
      TestBed.configureTestingModule({
        imports: [ base.imports() ],
        providers: [base.providers()],
      declarations: [ AddModuleComponent, ErrorMessageComponent, LoaderComponent, AddQuestionComponent ]
    })
    TestBed.overrideModule(
      BrowserDynamicTestingModule, {
        set: {
          entryComponents: [base.entryComponents(), AddQuestionComponent]
        }
      }
    )
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddModuleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
