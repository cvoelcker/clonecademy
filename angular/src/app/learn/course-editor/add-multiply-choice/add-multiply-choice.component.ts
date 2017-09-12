import {Component} from '@angular/core';

import {AddQuestionModule} from "../add-question/add-question.module"

import {slideIn} from "../../../animations";

import {MdDialog, MdDialogRef} from '@angular/material';
import {ImageCropperDialogComponent} from '../../../image-cropper/image-cropper.component';

@Component({
  selector: 'app-add-multiply-choice',
  templateUrl: './add-multiply-choice.component.html',
  styleUrls: ['./add-multiply-choice.component.scss'],
  animations: [slideIn],
})
export class AddMultiplyChoiceComponent extends AddQuestionModule {

  body = {
    answers: [{text: "", is_correct: true, visible: true, id: null, img: ''}],
    question_image: '',
    feedback_image: ''
  }

  url: string = "";

  constructor(public dialog: MdDialog) {
    super()
  }

  compInfo: string = "Loading";

  file: any = null;

  openImageDialog(width: number, height: number, key: string, answers = false) {
    let dialogRef = this.dialog.open(ImageCropperDialogComponent, {
      data: {
        width: width,
        height: height
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        if (answers) {
          this.body.answers[key].img = result
        }
        else {
          this.body[key] = result
        }

      }
    });
  }


  // the function to save it returns a object
  // {type: string, answers: [text: string, is_correct: boolean]}
  save(form): any {
    this.form = form;
    let answers = this.body.answers
    for (let i = 0; i < answers.length; i++) {
      if (answers[i].img == null) {
        answers[i].img = ""
      }
      delete answers[i].visible
    }
    return {
      type: "multiple_choice",
      question_image: this.body.question_image,
      feedback_image: this.body.feedback_image,
      answers: answers
    };
  }

  removeAnswer(event, index: number) {
    if (this.body.answers[index] != null && this.body.answers[index].visible == false) {
      this.body.answers.splice(index, 1);
    }
  }

  slideInFunction(index: number) {
    this.body['answers'][index].visible = false;
  }

  addAnswer() {
    this.body.answers.push({
      text: "",
      is_correct: false,
      visible: true,
      id: null,
      img: ""
    })
  }

  validAnswer(): boolean {
    for (let i = 0; i < this.body.answers.length; i++) {
      if (this.body.answers[i].is_correct) {
        return true;
      }
    }
    return false;
  }

}
