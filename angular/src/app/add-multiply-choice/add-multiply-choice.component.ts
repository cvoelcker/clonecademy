import { Component} from '@angular/core';

import { AddQuestionModule } from "../add-question/add-question.module"

@Component({
  selector: 'app-add-multiply-choice',
  templateUrl: './add-multiply-choice.component.html',
  styleUrls: ['./add-multiply-choice.component.scss']
})
export class AddMultiplyChoiceComponent extends AddQuestionModule {


  question: string;
  answers: [{text: string, correct: boolean}] = [{text: "", correct: true}];

  // the function to save it returns a object
  // {type: string, question: string, answers: [text: string, correct: boolean]}
  save(): any{
    return {
      type: "MultiplyChoiceQuestion",
      question: this.question,
      answers: this.answers
    };
  }

  removeAnswer(index: number){
    this.answers.splice(index, 1);
  }

  addAnswer(){
    this.answers.push({text: "", correct:false})
  }

}
