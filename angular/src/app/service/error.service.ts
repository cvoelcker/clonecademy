import {Injectable} from '@angular/core';

import {ErrorMessageComponent} from '../error-message/error-message.component'
import {MdDialog} from '@angular/material';

@Injectable()
export class ErrorDialog {


  constructor(private dialog: MdDialog) {
  }

  open(text: string) {
    let dialogRef = this.dialog.open(ErrorMessageComponent, {
      data: text
    })
  }


}
