import { Component, OnInit, ChangeDetectorRef, Output, EventEmitter, Input, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router'
import { ServerService } from "../service/server.service"

import { MultipleChoiceQuestionComponent } from "../multiple-choice-question/multiple-choice-question.component"

import { QuestionModule } from "./question.module"

@Component({
  selector: 'app-question',
  templateUrl: './question.component.html',
  styleUrls: ['./question.component.scss']
})
export class QuestionComponent implements OnInit {

  components = {
    MultipleChoiceQuestion: MultipleChoiceQuestionComponent
  }

  @ViewChild('question', {read: ViewContainerRef}) question: ViewContainerRef;
  moduleIndex: number;
  courseID: number;
  questionIndex: number;
  title: string;
  questionBody: string;
  questionFactory: ComponentFactory<any>;
  questionModule: QuestionModule;
  lastQuestion: boolean;
  lastModule: boolean;
  submitSend: boolean;
  submitCorrect: boolean;
  feedback: string;

  constructor(private changeDet: ChangeDetectorRef, private router: Router, public server: ServerService, private route: ActivatedRoute, private factory: ComponentFactoryResolver) {

  }

  ngAfterViewInit(){
  }

  ngOnInit(){

    this.route.params.subscribe((data: Params) => {
      this.courseID = data.id,
      this.moduleIndex = data.module,
      this.questionIndex = data.question
    })

    this.loadQuestion()

  }

  loadQuestion(){
    this.server.get("courses/"+this.courseID+"/"+this.moduleIndex + "/" + this.questionIndex).then(data => {

      this.submitCorrect = false;
      this.title = data.title
      this.questionBody = data.question_body
      this.lastQuestion = data.lastQuestion
      this.lastModule = data.lastModule
      // create Question based on the class
      this.questionFactory = this.factory.resolveComponentFactory(this.components[data.class])

      // empty question factory box bevor adding new stuff
      this.question.clear()
      let question = this.question.createComponent(this.questionFactory)
      this.questionModule = (<QuestionModule> question.instance)
      this.changeDet.detectChanges()

    })
  }


  submit(){

    let data = this.questionModule.submit();
    this.server.post("courses/"+this.courseID+"/"+this.moduleIndex + "/" + this.questionIndex, data)
      .then(data => this.evaluteAnswer(data))
      .catch(err => console.log(err))
  }

  evaluteAnswer(data){
    this.submitCorrect = data['evaluate']
    this.submitSend = true;

    if(data['feedback']){
      this.feedback = data['feedback']
    }
    else{
      this.feedback = "gut gemacht"
    }
  }

  next(){
    let module = Number(this.moduleIndex);
    let question = Number(this.questionIndex);
    if(!this.lastQuestion){
      question ++
    }
    else if(!this.lastModule){
      module ++
      question = 1;
    }
    else{
      // TODO add a feedback for the course here
      this.router.navigateByUrl("/course")
      return
    }
    this.router.navigateByUrl("/course/"+this.courseID+"/"+ module + "/" + question)
    this.moduleIndex = module;
    this.questionIndex = question
    this.loadQuestion()
  }

}
