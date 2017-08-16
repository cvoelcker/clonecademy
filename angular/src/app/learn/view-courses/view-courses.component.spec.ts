import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Http, RequestOptions } from '@angular/http';
import { Router, ActivatedRoute } from '@angular/router';

import { CourseViewComponent } from './view-courses.component';

describe('StaticPageComponent', () => {
  let component: CourseViewComponent;
  let fixture: ComponentFixture<CourseViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CourseViewComponent ],
      providers: [Http, RequestOptions, Router, ActivatedRoute]
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
