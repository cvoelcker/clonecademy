import { Component} from '@angular/core';

import { AddQuestionModule } from "../add-question/add-question.module"

import { slideIn } from "../../../animations";

@Component({
  selector: 'app-add-multiply-choice',
  templateUrl: './add-multiply-choice.component.html',
  styleUrls: ['./add-multiply-choice.component.scss'],
  animations: [ slideIn ]
})
export class AddMultiplyChoiceComponent extends AddQuestionModule {


  answers: Array<{text: string, is_correct: boolean, visible: boolean}> = [{text: "", is_correct: true, visible: true}];


  // the function to save it returns a object
  // {type: string, question: string, answers: [text: string, is_correct: boolean]}
  save(form): any{
    this.form = form;
    let answers = this.answers
    for(let i = 0; i < answers.length; i++){
      delete answers[i].visible
    }
    return {
      type: "MultiplyChoiceQuestion",
      question: this.question,
      answers: answers
    };
  }

  removeAnswer(event, index: number){
    if(this.answers[index] != null && this.answers[index].visible == false){
      this.answers.splice(index, 1);
    }
  }

  slideInFunction(index: number){
    this.answers[index].visible = false;
  }

  addAnswer(){
    this.answers.push({text: "", is_correct:false, visible: true})
  }

  validAnswer(): boolean{
    for(let i = 0; i < this.answers.length; i++){
      if(this.answers[i].is_correct){
        return true;
      }
    }
    return false;
  }

}
