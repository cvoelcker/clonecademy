import { Component, Type, Output, EventEmitter, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory } from '@angular/core';

import { AddQuestionModule } from './add-question.module'

@Component({
  selector: 'app-add-question',
  templateUrl: './add-question.component.html',
  styleUrls: ['./add-question.component.scss']
})
export class AddQuestionComponent {

  @Output() emitter: EventEmitter<any> = new EventEmitter();
  public child: Type<AddQuestionModule>;
  @ViewChild('question', {read: ViewContainerRef}) question: ViewContainerRef;
  questionFactory: ComponentFactory<AddQuestionModule>;

  questionCopy: AddQuestionModule

  feedback: string;
  feedbackBool: boolean;

  form = null;

  setForm(f){
    this.form = f;
  }

  constructor(private factory: ComponentFactoryResolver) { }

  // add a question to the view
  addQuestion(){
    // create factory
    // in the module class child will be set to the question type
    this.questionFactory = this.factory.resolveComponentFactory(this.child)
    // create new question
    let question = this.question.createComponent(this.questionFactory)

    this.questionCopy  = (<AddQuestionModule> question.instance)
  }



  remove(){
    this.emitter.emit("remove")
  }

  save(f): any{
    let response = this.questionCopy.save(f)
    response['feedbackBool'] = this.feedbackBool
    // check if custom feedback is set and save it if needed
    if(this.feedbackBool){
      response['feedback'] = this.feedback;
    }

    return response
  }

}
