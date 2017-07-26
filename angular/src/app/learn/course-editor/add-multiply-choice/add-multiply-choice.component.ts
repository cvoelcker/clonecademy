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
    answers: [{text: "", is_correct: true, visible: true, id: null}],
    question_image: '',
    answer_image: ''
  }

  url: string = "";

  compInfo: string = "Loading";

  file: any = null;

  questionImage(event):void {
    if(event.target.files && event.target.files[0]){

      //new fileReader
      var fileReader = new FileReader();
      //try to read file, this part does not work at all, need a solution
      fileReader.onload =(e) => {
        this.body.question_image = e.target['result']

      }

      fileReader.readAsDataURL(event.target.files[0])
    }
	}

  answerImage(event):void {
    if(event.target.files && event.target.files[0]){

      //new fileReader
      var fileReader = new FileReader();
      //try to read file, this part does not work at all, need a solution
      fileReader.onload =(e) => {
        this.body.answer_image = e.target['result']

      }

      fileReader.readAsDataURL(event.target.files[0])
    }
	}

  triggerFile(fileInput){
    fileInput.click()
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
      question_image: this.body.question_image,
      answer_image: this.body.answer_image,
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
