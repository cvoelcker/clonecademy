import {Component, Inject, Optional} from '@angular/core';

import {MD_DIALOG_DATA} from '@angular/material';

import {TranslateService} from '@ngx-translate/core';

@Component({
  selector: 'app-wrong-feedback-message',
  templateUrl: './wrong-feedback.component.html',
  styleUrls: ['./wrong-feedback.component.sass']
})
export class WrongFeedbackComponent {

  text = 'test';

  constructor(@Optional() @Inject(MD_DIALOG_DATA) public data: string, private translate: TranslateService) {
    if (data !== undefined) {
      translate.get(data['text']).subscribe((res) => {
        this.text = res
      })
    }
  }

}
