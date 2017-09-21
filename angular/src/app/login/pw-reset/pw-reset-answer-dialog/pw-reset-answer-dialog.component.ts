import { Component, Inject, Optional} from '@angular/core';
import { MdDialogRef, MD_DIALOG_DATA } from '@angular/material';

import {ServerService} from '../../../service/server.service';


/*
Dialog class for displaying the answer of the pw-reset request
Only used by the pw-reset component

@author Tobias Huber
*/
@Component({
  selector: 'app-pw-reset-answer-dialog',
  templateUrl: './pw-reset-answer-dialog.component.html',
  styleUrls: ['./pw-reset-answer-dialog.component.sass']
})
export class PwResetAnswerDialogComponent {

  loading = true;
  success = false;
  answer: any;
  error: any;


/*
When this dialog is constructed send a post request with the given data and handle
the response respectively

@author Tobias Huber
*/
  constructor(
    public dialogRef: MdDialogRef<PwResetAnswerDialogComponent>,
    private server: ServerService,
    @Inject(MD_DIALOG_DATA) public data: any,
  ) {
    this.loading = true;
    this.server.post('pw_reset/', this.data)
      .then(answer => {
        this.answer = answer;
        this.success = true;
        this.loading = false;
      })
      .catch(err => {
        if (err.status === 404) {
          this.error = 'This e-mail is unknown!'
        } else {
          this.error = err;
        }
        this.loading = false;
      })
  }
/*
  onNoClick(): void {
    console.log('onNoClick() was called')
    this.dialogRef.close();
  }
*/
}
