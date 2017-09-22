import {Component, OnInit, Input} from '@angular/core';

import {QuestionModuleComponent} from '../question/question.module'

@Component({
  selector: 'app-multiple-choice-question',
  templateUrl: './multiple-choice-question.component.html',
  styleUrls: ['./multiple-choice-question.component.scss']
})
export class MultipleChoiceQuestionComponent extends QuestionModuleComponent {

  // return array of the marked answers
  submit(): any {
    const sendAnswer = [];
    for (const ans of this.data.answers) {
      if (ans.value) {
        sendAnswer.push(ans.id)
      }
    }
    return sendAnswer;

  }

}
