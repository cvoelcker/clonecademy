import {Component, Inject, Optional, OnInit} from '@angular/core';

import {MD_DIALOG_DATA, MdDialogRef} from '@angular/material';


@Component({
  selector: 'app-error-message',
  templateUrl: './submit-delete.component.html',
  styleUrls: ['./submit-delete.component.scss']
})
export class SubmitDeleteComponent {


  constructor(
    @Optional() @Inject(MD_DIALOG_DATA) public data: any,
    private dialogRef: MdDialogRef<SubmitDeleteComponent>,
  ) {
  }

  delete() {
    this.dialogRef.close({delete: true})
  }
}
