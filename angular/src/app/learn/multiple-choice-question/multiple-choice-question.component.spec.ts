import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';

import { CourseComponent } from '../course/course.component';

import { BaseTest } from '../../base-test';

import { QuestionComponent } from '../question/question.component';

import { MultipleChoiceQuestionComponent } from './multiple-choice-question.component';

describe('Info Text Component', () => {
  let component: QuestionComponent;
  let fixture: ComponentFixture<QuestionComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [ base.imports() ],
      providers: [base.providers()],
      declarations: [ base.entryComponents([QuestionComponent, CourseComponent, MultipleChoiceQuestionComponent]) ]
    })
    TestBed.overrideModule(
      BrowserDynamicTestingModule, {
        set: {
          entryComponents: [base.entryComponents([MultipleChoiceQuestionComponent])]
        }
      }
    )
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(QuestionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('create', () => {
    component.setupQuestion({title: "test", body: "question", learning_text: 'learn', type:"multiple_choice", last_question: false, last_module: false, question_body: {}})
    expect(component.question).toBeTruthy()
    expect(component.questionModule instanceof MultipleChoiceQuestionComponent).toBeTruthy()
  });
});
