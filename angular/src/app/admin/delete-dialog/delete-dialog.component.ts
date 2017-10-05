import {Component, Inject, Optional} from '@angular/core';

import {MdDialogRef, MD_DIALOG_DATA} from '@angular/material';

import {ServerService} from '../../service/server.service';

@Component({
  selector: 'app-delete-dialog',
  templateUrl: './delete-dialog.component.html',
  styleUrls: ['./delete-dialog.component.sass']
})
export class DeleteDialogComponent {

  constructor(
    @Inject(MD_DIALOG_DATA) public data: any,
    private dialogRef: MdDialogRef<DeleteDialogComponent>,
    private server: ServerService,
  ) { }

  delete() {
    this.server.post('get-course-categories/', {delete: true, id: this.data['id']})
      .then(data => {
        this.dialogRef.close({deleted: true})
      })
  }
}
;
