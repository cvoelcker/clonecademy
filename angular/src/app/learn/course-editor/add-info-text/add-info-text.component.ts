import { Component} from '@angular/core';

import { AddQuestionModule } from "../add-question/add-question.module"

import { slideIn } from "../../../animations";

@Component({
  selector: 'app-add-info-text',
  templateUrl: './add-info-text.component.html',
  styleUrls: ['./add-info-text.component.scss'],
  animations: [ slideIn ],
})
export class AddInformationTextComponent extends AddQuestionModule {

  body = {
    visible: '',
  }

  url: string = "";

  constructor(){
    super()
  }

  compInfo: string = "Loading";


  // the function to save it returns a object
  // {type: string, answers: [text: string, is_correct: boolean]}
  save(form): any{
    this.form = form;
    return {
      type: "info_text",
      visible: this.body.visible,
    };
  }
}
