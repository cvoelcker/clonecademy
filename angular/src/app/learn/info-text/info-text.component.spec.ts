import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';

import {CourseComponent} from '../course/course.component';

import {BaseTest} from '../../base-test';

import {QuestionComponent} from '../question/question.component';

import {InformationTextComponent} from './info-text.component';

describe('Info Text Component', () => {
  let component: QuestionComponent;
  let fixture: ComponentFixture<QuestionComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [base.imports()],
      providers: [base.providers()],
      declarations: [base.entryComponents([QuestionComponent, CourseComponent, InformationTextComponent])]
    })
    TestBed.overrideModule(
      BrowserDynamicTestingModule, {
        set: {
          entryComponents: [base.entryComponents([InformationTextComponent])]
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
    component.setupQuestion({
      title: "test",
      body: "question",
      learning_text: 'learn',
      type: "info_text",
      last_question: false,
      last_module: false,
      question_body: {text_field: "info text", img: ""}
    })
    expect(component.question).toBeTruthy()
    expect(component.questionModule instanceof InformationTextComponent).toBeTruthy()
  });

  it('check text', () => {
    component.setupQuestion({
      title: "test",
      body: "question",
      learning_text: 'learn',
      type: "info_text",
      last_question: false,
      last_module: false,
      question_body: {text_field: "info text", img: ""}
    })
    expect(component.question).toBeTruthy()
    expect(component.questionModule).toBeTruthy()
  });
});
