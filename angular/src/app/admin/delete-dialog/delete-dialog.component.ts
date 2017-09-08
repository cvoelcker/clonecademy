import { Component, Inject, Optional } from '@angular/core';

import {MD_DIALOG_DATA} from '@angular/material';

@Component({
  selector: 'app-delete-dialog',
  templateUrl: './delete-dialog.component.html',
  styleUrls: ['./delete-dialog.component.sass']
})
export class DeleteDialogComponent {

  courses: any;

  constructor(@Optional() @Inject(MD_DIALOG_DATA) public data: string) {
    if(data != undefined){
      this.courses=data
    }
  }

  ngOnInit() {
  }
};
