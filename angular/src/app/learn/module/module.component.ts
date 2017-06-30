import { Component, OnInit, ComponentFactoryResolver, ViewChild } from '@angular/core';

import { ActivatedRoute, Params, Router } from '@angular/router'
import { ServerService } from '../../service/server.service';

import { ModuleDirective } from '../../directive/module.directive'


import { QuestionComponent } from "../question/question.component"
import { MultipleChoiceQuestionComponent } from "../multiple-choice-question/multiple-choice-question.component"

@Component({
  selector: 'app-module',
  templateUrl: './module.component.html',
  styleUrls: ['./module.component.scss']
})
export class ModuleComponent implements OnInit {

  components = {
    "MultipleChoiceQuestion" : MultipleChoiceQuestionComponent
    // add new qustion types here
  }
  name: any;
  courseID: number;
  moduleIndex: number;
  title: string;
  questionBody: string;
  lastModule:boolean;
  questions: any;
  learningText: string;

  constructor(private server: ServerService, private route: ActivatedRoute) {
    this.server.get("courses/"+this.courseID+"/"+this.moduleIndex).then(data => {
      this.name = data['name']
      this.questions = data['question'];
      this.learningText = data['learning_text'];
    })
  }

  ngOnInit(){
    this.route.params.subscribe((data: Params) => {this.courseID = data.id, this.moduleIndex = data.module})
  }


}
