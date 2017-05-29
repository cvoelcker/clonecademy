import { Component, OnInit} from '@angular/core';

import { AddQuestionComponent } from "../add-question/add-question.component"

@Component({
  selector: 'app-add-multiply-choice',
  templateUrl: './add-multiply-choice.component.html',
  styleUrls: ['./add-multiply-choice.component.css']
})
export class AddMultiplyChoiceComponent extends AddQuestionComponent {


  question: string;
  answers: [{text: string, correct: boolean}]

  ngOnInit() {
    this.answers = [{text: "test", correct: true}]
  }

  save(){
    return {type: "MultiplyChoiceQuestion", question: this.question, answers: this.answers}
  }

  addAnswer(){
    this.answers.push({text: "", correct:false})
  }

}
