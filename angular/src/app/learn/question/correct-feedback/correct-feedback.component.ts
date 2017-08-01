import { Component, Inject, Optional } from '@angular/core';

import {MD_DIALOG_DATA} from '@angular/material';

import {TranslateService} from '@ngx-translate/core';

@Component({
  selector: 'correct-feedback-message',
  templateUrl: './correct-feedback.component.html',
  styleUrls: ['./correct-feedback.component.sass']
})
export class CorrectFeedbackComponent {

  text: string;
  next: string

  constructor(@Optional() @Inject(MD_DIALOG_DATA) public data: string, private translate: TranslateService) {
    if(data != undefined){
      translate.get(data['text']).subscribe((res) => {this.text = res[data['text']]})
      this.next = data['next'];
    }
  }

  ngOnInit() {
  }

}
