import {Component, Inject, Optional} from '@angular/core';

import {MD_DIALOG_DATA} from '@angular/material';

@Component({
  selector: 'app-question-feedback',
  templateUrl: './question-feedback.component.html',
  styleUrls: ['./question-feedback.component.scss']
})
export class QuestionFeedbackComponent {


  constructor(@Inject(MD_DIALOG_DATA) public data: any) { }

}
