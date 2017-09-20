import {Component, OnInit} from '@angular/core';
import {FormGroup, FormControl, Validators, FormBuilder} from '@angular/forms';
import {Injectable} from '@angular/core';
import {MdDialog} from '@angular/material';

import {ServerService} from '../../service/server.service';
import {UserService} from '../../service/user.service';
import {ErrorDialog} from '../../service/error.service'
import {
  PwResetAnswerDialogComponent
} from './pw-reset-answer-dialog/pw-reset-answer-dialog.component';


@Component({
  selector: 'app-pw-reset',
  templateUrl: './pw-reset.component.html',
  styleUrls: ['./pw-reset.component.sass']
})
/*
component class for the password reset

@auther Tobias Huber
*/
@Injectable()
export class PwResetComponent {

  /*
  e-mail address for reset
   */
  newEmail: string;
  data: any;

  public registerForm = new FormGroup({
    email: new FormControl('email', Validators.email),
  })

  constructor(
    private errorDialog: ErrorDialog,
    private answerDialog: MdDialog,
    private server: ServerService,
    private fb: FormBuilder,
  ) {  }

  // validate input and open the answerDialog (that also sends the post request) if needed
  submit(form) {
    if (form.valid) {
      const answerDialogRef = this.answerDialog.open(PwResetAnswerDialogComponent, {
        // width: '400px',
        // height: '300px',
        data: {email: form.form.value['email']},
      });

      answerDialogRef.afterClosed().subscribe(result => {
        console.log('The dialog was closed');
      });
    }
  }
}
