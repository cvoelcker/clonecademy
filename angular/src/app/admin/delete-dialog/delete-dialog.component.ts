import {Component, Inject, Optional} from '@angular/core';

import {MdDialogRef, MD_DIALOG_DATA} from '@angular/material';

@Component({
  selector: 'app-delete-dialog',
  templateUrl: './delete-dialog.component.html',
  styleUrls: ['./delete-dialog.component.sass']
})
export class DeleteDialogComponent {

  courses: any;

  constructor(@Optional() public dialogRef: MdDialogRef<DeleteDialogComponent>, @Inject(MD_DIALOG_DATA) public data: string) {
    if (data != null) {
      this.courses = data
    } else {
      this.courses = {}
    }
  }

  onNoClick(): void {
    this.dialogRef.close();
  }
}
;
