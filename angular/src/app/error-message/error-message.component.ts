import {Component, Inject, Optional, OnInit} from '@angular/core';

import {MD_DIALOG_DATA} from '@angular/material';

import {TranslateService} from '@ngx-translate/core';

@Component({
  selector: 'app-error-message',
  templateUrl: './error-message.component.html',
  styleUrls: ['./error-message.component.sass']
})
export class ErrorMessageComponent implements OnInit {

  text: string;

  constructor(@Optional() @Inject(MD_DIALOG_DATA) public data: string, private translate: TranslateService) {
    if (data !== undefined) {
      translate.get(data).subscribe((res) => {
        this.text = res
      })
    }
  }
  ngOnInit(){
  }
}
