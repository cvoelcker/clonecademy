import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {BaseTest} from '../../../base-test';

import {AddInformationTextComponent} from './add-info-text.component';

describe('AddMultiplyChoiceComponent', () => {
  let component: AddInformationTextComponent;
  let fixture: ComponentFixture<AddInformationTextComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [base.imports()],
      providers: [base.providers()],
      declarations: [AddInformationTextComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddInformationTextComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
