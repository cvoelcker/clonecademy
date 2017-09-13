import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {Http} from '@angular/http';
import {Router, ActivatedRoute} from '@angular/router';

import {BaseTest} from '../base-test';

import {StaticPageComponent} from './static-page.component';

describe('StaticPage Component', () => {
  let component: StaticPageComponent;
  let fixture: ComponentFixture<StaticPageComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [base.imports()],
      declarations: [StaticPageComponent],
      providers: [base.providers()],
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StaticPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
