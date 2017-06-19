import { Component, OnInit, Input } from '@angular/core';

import { QuestionModule } from "../question/question.module"
import { ServerService } from "../service/server.service"

@Component({
  selector: 'app-MultipleChoiceQuestion',
  templateUrl: './multiple-choice-question.component.html',
  styleUrls: ['./multiple-choice-question.component.scss']
})
export class MultipleChoiceQuestionComponent extends QuestionModule {

  answers: [{id: number, text: string, value: boolean}];
  hightlightStatus: {};

  ngOnInit() {
    // to et the courseID, moduleIndex and questionIndex run ngOnInit from parent
    super.ngOnInit()

    this.server.get("courses/"+this.courseID+"/"+this.moduleIndex + "/" + this.questionIndex).then(data => {
      this.answers = data['answers']
      this.hightlightStatus = {}
      for(let ans of this.answers){
        this.hightlightStatus[ans.id] = false
      }
    })
  }

  submit(): any{
    let sendAnswer = [];
    for (let ans of this.answers){
      if(this.hightlightStatus[ans.id]){
        sendAnswer.push(ans.id)
      }
    }
    //super.submit
    return sendAnswer;

  }

}
