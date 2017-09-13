import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {FooterMainpageComponent} from './footer-mainpage.component';

describe('FooterMainpageComponent', () => {
  let component: FooterMainpageComponent;
  let fixture: ComponentFixture<FooterMainpageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [FooterMainpageComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FooterMainpageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
