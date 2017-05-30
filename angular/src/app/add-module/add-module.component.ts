import { Component, Type, OnInit, Output, EventEmitter, Input, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory } from '@angular/core';

import { AddQuestionComponent } from "../add-question/add-question.component"
import { AddQuestionModule } from "../add-question/add-question.module"

import { AddMultiplyChoiceComponent } from "../add-multiply-choice/add-multiply-choice.component"

@Component({
  selector: 'app-add-module',
  templateUrl: './add-module.component.html',
  styleUrls: ['./add-module.component.css']
})
export class AddModuleComponent implements OnInit {

  components: Array<{name: string, component: Type<AddQuestionModule>}> = [
    {name: "Multiple Choice Question", component: AddMultiplyChoiceComponent}
  ]
  selectedValue: Type<AddQuestionModule>;
  id: number;
  title: string;
  selected: boolean;
  question: ComponentFactory<AddQuestionModule>;
  questionArray: any[] = [];
  moduleComponent: AddQuestionModule;

  @ViewChild('module', {read: ViewContainerRef}) module: ViewContainerRef;

  @Output() clear: EventEmitter<any> = new EventEmitter();
  constructor(private factory: ComponentFactoryResolver) {

  }

  addQuestion(){
    if(this.selectedValue != undefined){
      this.question = this.factory.resolveComponentFactory(this.selectedValue)

      // add the question to the module component and add it to the array so we can edit and save it later
      let question = this.module.createComponent(this.question)
      let questionComponent = (<AddQuestionModule> question.instance)
      this.questionArray.push(questionComponent)
    }
  }

  ngOnInit() {
  }

  close(){
    this.clear.emit("remove")
  }

  up(){
    this.clear.emit("up")
  }

  down(){
    this.clear.emit("down")
  }

  save(){
    console.log(this.module)
    console.log(this.questionArray)
    for(let i = 0; i < this.module.length; i++){
      console.log(this.module.get(i))
    }
  }

}
