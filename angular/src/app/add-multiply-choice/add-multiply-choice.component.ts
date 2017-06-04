import { Component, OnInit} from '@angular/core';

import { AddQuestionModule } from "../add-question/add-question.module"

@Component({
  selector: 'app-add-multiply-choice',
  templateUrl: './add-multiply-choice.component.html',
  styleUrls: ['./add-multiply-choice.component.scss']
})
export class AddMultiplyChoiceComponent extends AddQuestionModule {


  question: string;
  answers: [{text: string, correct: boolean}];

  ngOnInit() {
    this.answers = [{text: "test", correct: true}]
  }

  save(): any{
    return {
      type: "MultiplyChoiceQuestion",
      question: this.question,
      answers: this.answers
    };
  }

  addAnswer(){
    this.answers.push({text: "", correct:false})
  }

}
