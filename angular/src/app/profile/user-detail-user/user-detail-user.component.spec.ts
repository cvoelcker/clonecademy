import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {BaseTest} from '../../base-test';

import {UserDetailUserComponent} from './user-detail-user.component';

describe('User Detail Component', () => {
  let component: UserDetailUserComponent;
  let fixture: ComponentFixture<UserDetailUserComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [base.imports()],
      providers: [base.providers()],
      declarations: [UserDetailUserComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UserDetailUserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
