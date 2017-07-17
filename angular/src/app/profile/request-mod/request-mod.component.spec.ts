import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BaseTest } from '../../base-test';

import { RequestModComponent } from './request-mod.component';


describe('RequestModComponent', () => {
  let component: RequestModComponent;
  let fixture: ComponentFixture<RequestModComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [ base.imports() ],
      providers: [ base.providers() ],
      declarations: [
        RequestModComponent
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RequestModComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
