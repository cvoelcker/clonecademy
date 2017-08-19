import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BaseTest } from '../../base-test';

import { CourseViewComponent } from './view-courses.component';

describe('CourseViewComponent', () => {
  let component: CourseViewComponent;
  let fixture: ComponentFixture<CourseViewComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [ base.imports() ],
      providers: [base.providers()],
      declarations: [ CourseViewComponent ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CourseViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
