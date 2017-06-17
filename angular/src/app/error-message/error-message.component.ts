import { Component, Inject } from '@angular/core';

import {MD_DIALOG_DATA} from '@angular/material';

@Component({
  selector: 'app-error-message',
  templateUrl: './error-message.component.html',
  styleUrls: ['./error-message.component.sass']
})
export class ErrorMessageComponent {

  constructor(@Inject(MD_DIALOG_DATA) public data: string) { }

  ngOnInit() {
  }

}
