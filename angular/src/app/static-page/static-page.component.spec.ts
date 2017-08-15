import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Http, RequestOptions } from '@angular/http';
import { Router, ActivatedRoute } from '@angular/router';

import { StaticPageComponent } from './static-page.component';

describe('StaticPageComponent', () => {
  let component: StaticPageComponent;
  let fixture: ComponentFixture<StaticPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StaticPageComponent ],
      providers: [Http, RequestOptions, Router, ActivatedRoute]
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
