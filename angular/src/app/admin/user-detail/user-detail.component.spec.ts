import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BaseTest } from '../../base-test';

import { UserDetailComponent } from './user-detail.component';

describe('AdminPageComponent', () => {
  let component: UserDetailComponent;
  let fixture: ComponentFixture<UserDetailComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
      TestBed.configureTestingModule({
        imports: [ base.imports() ],
        providers: [base.providers()],
      declarations: [ UserDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UserDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
