import {Component, OnInit, ViewChild, Optional, Inject} from '@angular/core';

import {MdDialogRef} from '@angular/material';

import {MD_DIALOG_DATA} from '@angular/material';


import {ImageCropperComponent, CropperSettings} from 'ng2-img-cropper';

@Component({
  selector: 'app-image-cropper',
  templateUrl: './image-cropper.component.html',
  styleUrls: ['./image-cropper.component.sass'],
})

export class ImageCropperDialogComponent {

  data: any;

  @ViewChild('cropper', undefined) cropper: ImageCropperComponent;

  cropperSettings: CropperSettings;

  constructor(@Optional() @Inject(MD_DIALOG_DATA) public input: { height: number, width: number }, public dialogRef: MdDialogRef<ImageCropperDialogComponent>) {
    this.cropperSettings = new CropperSettings();
    this.cropperSettings.noFileInput = true;
    this.cropperSettings.fileType = "image/*"
    if (input.width && input.height) {
      this.cropperSettings.canvasWidth = 500;
      this.cropperSettings.canvasHeight = 300;
      this.cropperSettings.croppedWidth = input.width;
      this.cropperSettings.croppedHeight = input.height;
    }
    this.data = {};
  }

  fileChangeListener($event) {
    this.cropper.reset()
    var image: any = new Image();
    var file: File = $event.target.files[0];
    var myReader: FileReader = new FileReader();
    var that = this;
    myReader.onloadend = function (loadEvent: any) {
      image.src = loadEvent.target.result;
      that.cropper.setImage(image);
    };
    myReader.readAsDataURL(file);
  }


}
