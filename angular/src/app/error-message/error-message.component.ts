import {Component, Inject, Optional, OnInit} from '@angular/core';

import {MD_DIALOG_DATA} from '@angular/material';

@Component({
  selector: 'app-error-message',
  templateUrl: './error-message.component.html',
  styleUrls: ['./error-message.component.sass']
})
export class ErrorMessageComponent {

  keys: Array<string>;

  constructor(@Optional() @Inject(MD_DIALOG_DATA) public data: any) {
    if(typeof data !== "string"){
      this.keys = Object.keys(data)
    }
  }
}
