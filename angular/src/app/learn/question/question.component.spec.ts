import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';

import {CourseComponent} from '../course/course.component';

import {BaseTest} from '../../base-test';

import {QuestionComponent} from './question.component';

import {InformationTextComponent} from '../info-text/info-text.component';

describe('Question Component', () => {
  let component: QuestionComponent;
  let fixture: ComponentFixture<QuestionComponent>;

  beforeEach(async(() => {
    const base = new BaseTest();
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

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
