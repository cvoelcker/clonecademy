import {Component, Inject, Optional, OnInit} from '@angular/core';

import {MD_DIALOG_DATA} from '@angular/material';

@Component({
  selector: 'app-quiz-end-popup',
  templateUrl: './quiz-end-popup.component.html',
  styleUrls: ['./quiz-end-popup.component.scss']
})
export class QuizEndPopupComponent {

  constructor(@Optional() @Inject(MD_DIALOG_DATA) public data: any) {
    console.log(data)
  }
}
