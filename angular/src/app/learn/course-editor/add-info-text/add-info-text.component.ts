import {Component} from '@angular/core';

import {AddQuestionModuleComponent} from '../add-question/add-question.module'

import {slideIn} from '../../../animations';

import {MdDialog, MdDialogRef} from '@angular/material';
import {ImageCropperDialogComponent} from '../../../image-cropper/image-cropper.component';


@Component({
  selector: 'app-add-info-text',
  templateUrl: './add-info-text.component.html',
  styleUrls: ['./add-info-text.component.scss'],
  animations: [slideIn],
})
/**
 @title: AddInformationTextComponent
 @author: Claas Voelcker

 This component is used to add an information text between questions.
 */
export class AddInformationTextComponent extends AddQuestionModuleComponent {
  body = {
    text_field: '',
    image: '',
  };
  compInfo = 'Loading';
  url = '';

  constructor(public dialog: MdDialog) {
    super()
  }

  // the function to save it returns a object
  // {type: string, answers: [text: string, is_correct: boolean]}
  save(form): any {
    this.form = form;
    return {
      type: 'info_text',
      text_field: this.body.text_field,
      image: this.body.image,
    };
  }

  openImageDialog(width: number, height: number, key: string) {
    const dialogRef = this.dialog.open(ImageCropperDialogComponent, {
      data: {
        width: width,
        height: height
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.body[key] = result
      }
    });
  }
}
