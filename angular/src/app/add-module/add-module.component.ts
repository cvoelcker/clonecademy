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
      this.questionArray.push(question)
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
    let values = [];
    for(let i = 0; i < this.questionArray.length; i++){
      let tmp = this.questionArray[i];
      let index = this.module.indexOf(this.questionArray[i].hostView)

      let save = (<AddQuestionModule> tmp.instance).save()
      save['order'] = index;
      values.push(save)
    }
    return {title: this.title, question: values};
  }

}
