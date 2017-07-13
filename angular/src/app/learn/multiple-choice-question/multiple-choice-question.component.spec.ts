import { async, ComponentFixture, TestBed } from '@angular/core/testing';


import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';

import { BaseTest } from '../../base-test';

import { MultipleChoiceQuestionComponent } from './multiple-choice-question.component';

describe('MultipleChoiceQuestionComponent', () => {
  let component: MultipleChoiceQuestionComponent;
  let fixture: ComponentFixture<MultipleChoiceQuestionComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
      TestBed.configureTestingModule({
        imports: [ base.imports() ],
        providers: [base.providers()],
        declarations: [ base.entryComponents([MultipleChoiceQuestionComponent]) ]
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
    fixture = TestBed.createComponent(MultipleChoiceQuestionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
