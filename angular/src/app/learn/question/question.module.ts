import { Component, Input } from '@angular/core';
import { ServerService } from "../../service/server.service"
import { ActivatedRoute, Params } from '@angular/router'


@Component({
  selector: 'app-MultipleChoiceQuestion',
  template: '<p>Implement me</p>',
})
export class QuestionModule{

  questionText: string;
  moduleIndex: number;
  questionIndex: number
  courseID: number;
  feedback: any;

  data: any;

  disable = false;

  constructor(public server: ServerService, private route: ActivatedRoute) {
  }

  // this has to be set on every subfunction
  submit(): any{
    return "test";
  }

  // after succesfull submit this function will be called to deactivate buttons
  block(): void{
    this.disable = true;
  }
 }
