import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {BaseTest} from '../base-test';
import {MdDialog, MdDialogRef} from '@angular/material';


import {ImageCropperComponent, CropperSettings} from 'ng2-img-cropper';

import {ImageCropperDialogComponent} from './image-cropper.component';

describe('ImageCropperDialogComponent', () => {
  let component: ImageCropperDialogComponent;
  let fixture: ComponentFixture<ImageCropperDialogComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [base.imports()],
      declarations: [ImageCropperDialogComponent, ImageCropperComponent],
      providers: [base.providers(), MdDialog, MdDialogRef],
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ImageCropperDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // it('should be created', () => {
  //   expect(component).toBeTruthy();
  // });
});
