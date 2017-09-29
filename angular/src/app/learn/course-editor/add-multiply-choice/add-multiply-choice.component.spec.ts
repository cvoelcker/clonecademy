import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {BaseTest} from '../../../base-test';

import {AddMultiplyChoiceComponent} from './add-multiply-choice.component';

describe('AddMultiplyChoiceComponent', () => {
  let component: AddMultiplyChoiceComponent;
  let fixture: ComponentFixture<AddMultiplyChoiceComponent>;

  beforeEach(async(() => {
    const base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [base.imports()],
      providers: [base.providers()],
      declarations: [AddMultiplyChoiceComponent]
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
