import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {BaseTest} from '../../base-test';

import {ProfilesComponent} from './profiles.component';

describe('ProfilesComponent', () => {
  let component: ProfilesComponent;
  let fixture: ComponentFixture<ProfilesComponent>;

  beforeEach(async(() => {
    const base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [base.imports()],
      providers: [base.providers()],
      declarations: [ProfilesComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfilesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
    console.log(component)
  });
});
