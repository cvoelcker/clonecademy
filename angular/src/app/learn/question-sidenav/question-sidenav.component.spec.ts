import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {BaseTest} from '../../base-test';

import {SassHelperComponent} from '../../service/sass-helper/sass-helper'

import {ChartsModule} from 'ng2-charts';

import {QuestionSidenavComponent} from './question-sidenav.component';

describe('QuestionSidenavComponent', () => {
  let component: QuestionSidenavComponent;
  let fixture: ComponentFixture<QuestionSidenavComponent>;

  beforeEach(async(() => {
    const base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [base.imports(), ChartsModule],
      providers: [base.providers()],
      declarations: [QuestionSidenavComponent, SassHelperComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(QuestionSidenavComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
