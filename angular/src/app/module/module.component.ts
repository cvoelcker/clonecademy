import { Component, OnInit, ComponentFactoryResolver, ViewChild } from '@angular/core';

import { ActivatedRoute, Params } from '@angular/router'
import { ServerService } from '../service/server.service';

import { ModuleDirective } from '../directive/module.directive'


import { QuestionComponent } from "../question/question.component"
import { MultipleChoiceQuestionComponent } from "../multiple-choice-question/multiple-choice-question.component"

@Component({
  selector: 'app-module',
  templateUrl: './module.component.html',
  styleUrls: ['./module.component.css']
})
export class ModuleComponent implements OnInit {

  components = {
    "MultipleChoiceQuestion" : MultipleChoiceQuestionComponent
    // add new qustion types here
  }
  module: any;
  courseID: number;
  moduleID: number;
  @ViewChild(ModuleDirective) adHost: ModuleDirective;

  constructor(private factory: ComponentFactoryResolver, private server: ServerService, private route: ActivatedRoute) { }

  ngOnInit(){
    this.route.params.subscribe((data: Params) => {this.courseID = data.id, this.moduleID = data.module})
    this.server.get("courses/"+this.courseID+"/"+this.moduleID).then(data => this.loadContainer(data))
  }


  loadContainer(value: any){
    let component = this.factory.resolveComponentFactory(this.components[value.class])

    let viewRef = this.adHost.viewContainerRef;
    viewRef.clear();
    let componenRef = viewRef.createComponent(component);

    let question = (<QuestionComponent> componenRef.instance);
    question.data = value;
    question.courseID = this.courseID;
    question.moduleID = this.moduleID;

  }

}
