import { Component, Type, OnInit, Output, EventEmitter, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory } from '@angular/core';

import { AddQuestionComponent } from "../add-question/add-question.component"


import { AddQuestionModule } from '../add-question/add-question.module'
import { AddMultiplyChoiceComponent } from "../add-multiply-choice/add-multiply-choice.component"

@Component({
  selector: 'app-add-module',
  templateUrl: './add-module.component.html',
  styleUrls: ['./add-module.component.scss']
})
export class AddModuleComponent implements OnInit {

  components: Array<{name: string, component: Type<AddQuestionModule>}> = [
    {name: "Multiple Choice Question", component: AddMultiplyChoiceComponent}
  ]
  selectedValue: Type<AddQuestionComponent>;
  id: number;
  title: string;
  learningText: string;
  selected: boolean;
  question: ComponentFactory<AddQuestionComponent>;
  questionArray: any[] = [];
  moduleComponent: AddQuestionComponent;

  @ViewChild('module', {read: ViewContainerRef}) module: ViewContainerRef;

  @Output() clear: EventEmitter<any> = new EventEmitter();
  constructor(private factory: ComponentFactoryResolver) {
    this.question = this.factory.resolveComponentFactory(AddQuestionComponent)
  }

  addQuestion(){
    if(this.selectedValue != undefined){

      // add the question to the module component and add it to the array so we can edit and save it later
      let question = this.module.createComponent(this.question)
      let q = (<AddQuestionComponent> question.instance)
      q.emitter.subscribe(data => this.module.detach())
      q.child = this.selectedValue
      q.addQuestion()
      this.questionArray.push(question)
    }
  }

  ngOnInit() {
  }

  // emit remove so parent class can remove this
  close(){
    this.clear.emit("remove")
  }

  // emit up so parent class can change the position
  up(){
    this.clear.emit("up")
  }

  // emit down so parent can change the position
  down(){
    this.clear.emit("down")
  }

  // save all questions in the correct order
  // append title, and the learning Text and return it
  save(){
    let values = [];
    for(let i = 0; i < this.questionArray.length; i++){
      let tmp = this.questionArray[i];
      let index = this.module.indexOf(this.questionArray[i].hostView)
      if(index >= 0){
        let save = (<AddQuestionComponent> tmp.instance).save()
        save['order'] = index;
        values.push(save)
      }

    }
    return {title: this.title, question: values, learningText: this.learningText};
  }

}
