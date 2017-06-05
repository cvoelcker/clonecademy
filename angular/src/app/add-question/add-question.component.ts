import { Component, Type, OnInit, Output, EventEmitter, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory } from '@angular/core';

import { AddQuestionModule } from './add-question.module'

@Component({
  selector: 'app-add-question',
  templateUrl: './add-question.component.html',
  styleUrls: ['./add-question.component.scss']
})
export class AddQuestionComponent implements OnInit {

  @Output() emitter: EventEmitter<any> = new EventEmitter();
  public child: Type<AddQuestionModule>;
  @ViewChild('question', {read: ViewContainerRef}) question: ViewContainerRef;
  questionFactory: ComponentFactory<AddQuestionModule>;

  questionCopy: AddQuestionModule

  feedback: string;
  feedbackBool: boolean;

  constructor(private factory: ComponentFactoryResolver) {
  }

  ngOnInit() {


  }

  addQuestion(){
    this.questionFactory = this.factory.resolveComponentFactory(this.child)
    let question = this.question.createComponent(this.questionFactory)

    this.questionCopy  = (<AddQuestionModule> question.instance)
  }

  remove(){
    this.emitter.emit("remove")
  }

  save(): any{
    let response = this.questionCopy.save()
    response['feedbackBool'] = this.feedbackBool
    if(this.feedbackBool){
      response['feedback'] = this.feedback;
    }

    return response
  }

}