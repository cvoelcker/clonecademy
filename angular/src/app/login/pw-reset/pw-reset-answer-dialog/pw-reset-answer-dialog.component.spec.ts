import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PwResetAnswerDialogComponent } from './pw-reset-answer-dialog.component';

describe('PwResetAnswerDialogComponent', () => {
  let component: PwResetAnswerDialogComponent;
  let fixture: ComponentFixture<PwResetAnswerDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PwResetAnswerDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PwResetAnswerDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
