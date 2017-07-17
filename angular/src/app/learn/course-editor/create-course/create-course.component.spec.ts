import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BaseTest } from '../../../base-test';
import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';

import { CourseService}  from '../../../service/course.service';

import { ErrorMessageComponent } from '../../../error-message/error-message.component';

import { AddModuleComponent } from '../add-module/add-module.component';

import { CreateCourseComponent } from './create-course.component';

describe('CreateCourseComponent', () => {
  let component: CreateCourseComponent;
  let fixture: ComponentFixture<CreateCourseComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
      TestBed.configureTestingModule({
      imports: [ base.imports() ],
      providers: [base.providers()],
      declarations: [ CreateCourseComponent, ErrorMessageComponent, AddModuleComponent ]
    })
    TestBed.overrideModule(
      BrowserDynamicTestingModule, {
        set: {
          entryComponents: [AddModuleComponent]
        }
      }
    )
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateCourseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
