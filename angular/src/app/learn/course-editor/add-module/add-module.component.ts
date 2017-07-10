import { Component, ElementRef, ChangeDetectorRef, Type, OnInit, Output, EventEmitter, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory } from '@angular/core';

import { AddQuestionComponent } from "../add-question/add-question.component"

import { slideIn } from "../../../animations";

import { AddQuestionModule } from '../add-question/add-question.module'
import { AddMultiplyChoiceComponent } from "../add-multiply-choice/add-multiply-choice.component"

@Component({
  selector: 'app-add-module',
  templateUrl: './add-module.component.html',
  styleUrls: ['./add-module.component.scss'],
  animations: [ slideIn ]
})
export class AddModuleComponent implements OnInit {

  components: Array<{name: string, component: Type<AddQuestionModule>}> = [
    {name: "Multiple Choice Question", component: AddMultiplyChoiceComponent}
  ]
  selectedValue: Type<AddQuestionComponent> = null;
  id: number;
  title: string = "";
  learningText: string = "";
  selected: boolean;
  question: ComponentFactory<AddQuestionComponent>;
  questionArray: any[] = [];
  moduleComponent: AddQuestionComponent;

  // the parent class set this to true when the save button is pressed
  form = null;

  loading = false;

  @ViewChild('module', {read: ViewContainerRef}) module: ViewContainerRef;

  @Output() clear: EventEmitter<any> = new EventEmitter();
  constructor(private ref: ChangeDetectorRef, private factory: ComponentFactoryResolver) {
    this.question = this.factory.resolveComponentFactory(AddQuestionComponent)
  }

  addQuestion(component){

      // add the question to the module component and add it to the array so we can edit and save it later
      let question = this.module.createComponent(this.question)
      let q = (<AddQuestionComponent> question.instance)
      q.form = this.form
      q.emitter.subscribe(data => this.module.detach())
      q.child = component
      q.addQuestion()
      this.questionArray.push(question)
      this.selectedValue = null;

  }

  ngOnInit() {
  }

  ngAfterViewInit(){
    this.loading = true;
    this.ref.detectChanges()
  }

  // emit remove so parent class can remove this
  close(){
    this.loading = false;
    //this.clear.emit("remove")
  }

  remove(event){
    if(event.toState == "0" && this.loading == false){
      this.clear.emit("remove")
    }
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
  // append title, and the module description and return it
  save(form){
    this.form = form;
    let values = [];
    for(let i = 0; i < this.questionArray.length; i++){
      let tmp = this.questionArray[i];
      let index = this.module.indexOf(this.questionArray[i].hostView)
      if(index >= 0){
        let save = (<AddQuestionComponent> tmp.instance).save(form)
        save['order'] = index;
        values.push(save)
      }
    }

    return {title: this.title, question: values, learningText: this.learningText};
  }

}
