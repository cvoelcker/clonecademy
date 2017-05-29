import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddMultiplyChoiceComponent } from './add-multiply-choice.component';

describe('AddMultiplyChoiceComponent', () => {
  let component: AddMultiplyChoiceComponent;
  let fixture: ComponentFixture<AddMultiplyChoiceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddMultiplyChoiceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddMultiplyChoiceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
