import { Component, OnInit, Input } from '@angular/core';

import { QuestionComponent } from "../question/question.component"
import { ServerService } from "../service/server.service"

@Component({
  selector: 'app-MultipleChoiceQuestion',
  templateUrl: './multiple-choice-question.component.html',
  styleUrls: ['./multiple-choice-question.component.css']
})
export class MultipleChoiceQuestionComponent implements QuestionComponent {

  @Input() data: any;
  moduleID: number;
  courseID: number;
  answers: [{"id": number, "text": string, "value": boolean}];
  hightlightStatus: {};

  constructor(public server: ServerService) {

   }

  ngOnInit() {
    this.answers = this.data.answers
    this.hightlightStatus = {}
    for(let ans of this.answers){
      this.hightlightStatus[ans.id] = false
    }
  }

  submit(): Promise<boolean>{
    let sendAnswer = [];
    for (let ans of this.answers){
      if(this.hightlightStatus[ans.id]){
        sendAnswer.push(ans.id)
      }
    }
    //super.submit
    return new Promise<boolean>((resolve, reject) => {
      this.server.post("courses/"+this.courseID+"/"+this.moduleID, sendAnswer).then(data => {
        if(data){
          resolve(data)
        }
        else{
          reject(data)
        }
      })

    })

  }

}
