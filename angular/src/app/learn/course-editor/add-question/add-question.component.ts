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

  questionCopy: AddQuestionModule;
  questionBody = "";
  feedback: string;
  feedbackBool: boolean;
  id: number;
  title: string;

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
  addQuestion(data){
    //console.log(answers)
    // create factory
    // in the module class child will be set to the question type
    this.questionFactory = this.factory.resolveComponentFactory(this.child)
    // create new question
    let question = this.question.createComponent(this.questionFactory)

    // set the question text
    
    this.questionBody = data["text"]
    this.title = data['title']
    let feedback = data['feedback']
    // check if the feedback is set and if true set the feedback text
    if(feedback != undefined && feedback != ""){
      this.feedbackBool = true;
      this.feedback = feedback
    }
    this.id = data['id'];

    this.questionCopy  = (<AddQuestionModule> question.instance)
    this.questionCopy.edit(data['question_body']);
  }



  remove(e){
    if(e != null && e.toState == "0"){
      //this.emitter.emit("remove")
    }
  }

  save(f): any{
    let response = this.questionCopy.save(f)
    // check if custom feedback is set and save it if needed

    response['id'] = this.id;

    response['text'] = this.questionBody;
    response['title'] = this.title
    if(this.feedbackBool){
      response['feedback'] = this.feedback;
    }
    else{
      response['feedback'] = ''
    }
    if(response['feedback'] == undefined){
      response['feedback'] = "";
    }

    return response
  }

}
