import { Component } from '@angular/core';

import {MdDialog, MdDialogRef } from '@angular/material';

import { UserService } from '../service/user.service'



@Component({
  selector: 'your-dialog-selector',
  templateUrl: './dialog.component.html',
  styleUrls: ['./dialog.component.scss']
})
export class DialogComponent {
  constructor(private user: UserService, public dialogRef: MdDialogRef<DialogComponent>) { }
}
