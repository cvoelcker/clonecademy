import { Component, Inject, Optional} from '@angular/core';
import { MdDialogRef, MD_DIALOG_DATA } from '@angular/material';

import {ServerService} from '../../../service/server.service';
import {UserService} from '../../../service/user.service';


/*
Dialog class for checking authorization again

@author Tobias Huber
*/
@Component({
  selector: 'app-auth-dialog',
  templateUrl: './auth-dialog.component.html',
  styleUrls: ['./auth-dialog.component.sass']
})
export class AuthDialogComponent {

  password: string;
  error = false;

/*
When this dialog is constructed send a post request with the given data and handle
the response respectively

@author Tobias Huber
*/
  constructor(
    public dialogRef: MdDialogRef<AuthDialogComponent>,
    private server: ServerService,
    private user: UserService,
    @Inject(MD_DIALOG_DATA) public data: any,
  ) {  }

  /*
  function that sends the final request
  */
  submit(pw: string) {
    this.data['oldpassword'] = pw;
    this.server.post('user/current', this.data, false, true).then(() => {
      this.user.setData(this.data);
      this.dialogRef.close();
      this.error = false;
    }).catch(err => {
      this.error = true;
    })
  }
}
