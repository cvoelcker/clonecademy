import {Component, Inject, Optional} from '@angular/core';

import {MD_DIALOG_DATA} from '@angular/material';

import {TranslateService} from '@ngx-translate/core';

@Component({
  selector: 'wrong-feedback-message',
  templateUrl: './wrong-feedback.component.html',
  styleUrls: ['./wrong-feedback.component.sass']
})
export class WrongFeedbackComponent {

  text: string = "test";

  constructor(@Optional() @Inject(MD_DIALOG_DATA) public data: string, private translate: TranslateService) {
    if (data != undefined) {
      console.log(data['text'])
      translate.get(data['text']).subscribe((res) => {
        this.text = res
      })
    }
  }

  ngOnInit() {
  }

}
