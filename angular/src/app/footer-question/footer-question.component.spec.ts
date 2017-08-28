import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FooterQuestionComponent } from './footer-question.component';

describe('FooterQuestionComponent', () => {
  let component: FooterQuestionComponent;
  let fixture: ComponentFixture<FooterQuestionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FooterQuestionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FooterQuestionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
