import { Component, OnInit, Input } from '@angular/core';
import { ServerService } from "../../service/server.service"
import { ActivatedRoute, Params } from '@angular/router'


@Component({
  selector: 'app-MultipleChoiceQuestion',
  template: '<p>Implement me</p>',
})
export class QuestionModule implements OnInit{

  questionText: string;
  moduleIndex: number;
  questionIndex: number
  courseID: number;

  data: any;

  disable = false;

  constructor(public server: ServerService, private route: ActivatedRoute) {
  }

  submit(): any{
    return "test";
  }

  block(): void{
    this.disable = true;
  }
  ngOnInit(){
    this.route.params.subscribe((data: Params) => {
      this.courseID = data.id,
      this.moduleIndex = data.module,
      this.questionIndex = data.question
    })
  }
 }
