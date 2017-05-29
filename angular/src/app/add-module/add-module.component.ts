import { Component, OnInit, Output, EventEmitter, Input, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory } from '@angular/core';

import { AddQuestionComponent } from "../add-question/add-question.component"

import { AddMultiplyChoiceComponent } from "../add-multiply-choice/add-multiply-choice.component"

@Component({
  selector: 'app-add-module',
  templateUrl: './add-module.component.html',
  styleUrls: ['./add-module.component.css']
})
export class AddModuleComponent implements OnInit {

  id: number;
  selected: boolean;
  multiplyChoice: ComponentFactory<AddMultiplyChoiceComponent>;

  moduleComponent: any;

  @ViewChild('module', {read: ViewContainerRef}) module: ViewContainerRef;

  @Output() clear: EventEmitter<any> = new EventEmitter();
  constructor(private factory: ComponentFactoryResolver) {
    this.multiplyChoice = factory.resolveComponentFactory(AddMultiplyChoiceComponent)
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

  chooseType(){
    this.selected = true;
    if(this.module != undefined){
      this.module.clear();
    }
    let course = this.module.createComponent(this.multiplyChoice)
    this.moduleComponent = (<AddQuestionComponent> course.instance)

  }
  save(){
    if(this.selected){
      return this.moduleComponent.save();
    }
    return null;
  }

}
