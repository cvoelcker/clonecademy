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

  body = {
    answers: [{text: "", is_correct: true, visible: true, id: null}]

  }


  // the function to save it returns a object
  // {type: string, answers: [text: string, is_correct: boolean]}
  save(form): any{
    this.form = form;
    let answers = this.body.answers
    for(let i = 0; i < answers.length; i++){
      delete answers[i].visible
    }
    return {
      type: "multiple_choice",
      answers: answers
    };
  }

  removeAnswer(event, index: number){
    if(this.body.answers[index] != null && this.body.answers[index].visible == false){
      this.body.answers.splice(index, 1);
    }
  }

  slideInFunction(index: number){
    this.body['answers'][index].visible = false;
  }

  addAnswer(){
    this.body.answers.push({text: "", is_correct:false, visible: true, id: null})
  }

  validAnswer(): boolean{
    for(let i = 0; i < this.body.answers.length; i++){
      if(this.body.answers[i].is_correct){
        return true;
      }
    }
    return false;
  }

}
