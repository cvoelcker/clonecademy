import { Component, OnInit, Type, Output, ChangeDetectorRef, EventEmitter, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory } from '@angular/core';

import { AddQuestionModule } from './add-question.module'
import { slideIn } from "../../../animations";

@Component({
  selector: 'app-add-question',
  templateUrl: './add-question.component.html',
  styleUrls: ['./add-question.component.scss'],
  animations: [ slideIn ]
})
export class AddQuestionComponent implements OnInit {

  @Output() emitter: EventEmitter<any> = new EventEmitter();
  public child: Type<AddQuestionModule>;
  @ViewChild('question', {read: ViewContainerRef}) question: ViewContainerRef;
  questionFactory: ComponentFactory<AddQuestionModule>;

  questionCopy: AddQuestionModule
  questionBody = "";
  feedback: string;
  feedbackBool: boolean;
  id: number;

  form = null;

  loading = false;

  ngOnInit(){
    this.loading = true;
    this.ref.detectChanges()
  }

  setForm(f){
    this.form = f;
  }

  constructor(private factory: ComponentFactoryResolver, private ref: ChangeDetectorRef) { }

  // add a question to the view
  addQuestion(id?: number, questionBody?: string, body?: any, feedback?: string){
    //console.log(answers)
    // create factory
    // in the module class child will be set to the question type
    this.questionFactory = this.factory.resolveComponentFactory(this.child)
    // create new question
    let question = this.question.createComponent(this.questionFactory)
    this.questionBody = questionBody

    this.id = id;

    this.questionCopy  = (<AddQuestionModule> question.instance)
    this.questionCopy.edit(body);
  }



  remove(e){
    if(e != null && e.toState == "0"){
      this.emitter.emit("remove")

    }
  }

  save(f): any{
    let response = this.questionCopy.save(f)
    // check if custom feedback is set and save it if needed
  
    response['id'] = this.id;

    response['body'] = this.questionBody;
    response['feedback'] = this.feedback;
    response['title'] = ""
    if(response['feedback'] == undefined){
      response['feedback'] = "";
    }

    return response
  }

}
