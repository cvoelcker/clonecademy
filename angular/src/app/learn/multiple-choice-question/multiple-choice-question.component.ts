import { Component, OnInit, Input } from '@angular/core';

import { QuestionModule } from "../question/question.module"

@Component({
  selector: 'app-MultipleChoiceQuestion',
  templateUrl: './multiple-choice-question.component.html',
  styleUrls: ['./multiple-choice-question.component.scss']
})
export class MultipleChoiceQuestionComponent extends QuestionModule {

  // return array of the marked answers
  submit(): any{
    let sendAnswer = [];
    for (let ans of this.data.answers){
      if(ans.value){
        sendAnswer.push(ans.id)
      }
    }
    //super.submit
    return sendAnswer;

  }

}
