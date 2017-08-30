import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BaseTest } from '../../../base-test';

import { AddInformationYoutubeComponent } from './add-info-youtube.component';

describe('AddInformationYoutubeComponent', () => {
  let component: AddInformationYoutubeComponent;
  let fixture: ComponentFixture<AddInformationYoutubeComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
      TestBed.configureTestingModule({
        imports: [ base.imports() ],
        providers: [base.providers()],
      declarations: [ AddInformationYoutubeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddInformationYoutubeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
