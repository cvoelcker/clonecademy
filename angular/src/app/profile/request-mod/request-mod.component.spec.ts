import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RequestModComponent } from './request-mod.component';

describe('RequestModComponent', () => {
  let component: RequestModComponent;
  let fixture: ComponentFixture<RequestModComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RequestModComponent ]
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
