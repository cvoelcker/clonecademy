import {
  Component,
  OnInit,
  OnDestroy,
  ChangeDetectorRef,
  Output,
  EventEmitter,
  Input,
  ViewChild,
  ViewContainerRef,
  ComponentFactoryResolver,
  ComponentFactory
} from '@angular/core';
import {trigger, state, style, animate, transition} from '@angular/animations';

import {ActivatedRoute, Params, Router} from '@angular/router'
import {ServerService} from '../../service/server.service'
import {MdDialog} from '@angular/material';

import {TranslateService} from '@ngx-translate/core';
import {MdSidenavModule} from '@angular/material';
import {MultipleChoiceQuestionComponent} from '../multiple-choice-question/multiple-choice-question.component'
import {InformationTextComponent} from '../info-text/info-text.component'

import {WrongFeedbackComponent} from './wrong-feedback/wrong-feedback.component';
import {QuestionModuleComponent} from './question.module';

import {QuestionDictionary} from '../question-dictionary';

import {Subject} from 'rxjs/Subject';

@Component({
  selector: 'app-question',
  templateUrl: './question.component.html',
  styleUrls: ['./question.component.scss'],
  animations: [trigger('slideIn', [
    state('1', style({
      'left': '0',
    })),
    state('0', style({
      'left': '-200px',
    })),
    transition('1 => 0', [
      style({left: '0'}),
      animate(250, style({left: '-200px'}))
    ]),
    transition('* => 1', [
      style({left: '-200px'}),
      animate(250, style({left: '0'})),
    ])])
  ]
})
export class QuestionComponent implements OnInit, OnDestroy {

  // QUESTION FACTORY COMPONENT
  components = QuestionDictionary.components

  @ViewChild('question', {read: ViewContainerRef}) question: ViewContainerRef;
  moduleIndex: number;
  courseID: number;
  questionIndex: number;
  // Module variables
  title: string;
  learning_text: string;

  questionBody: string;
  questionFactory: ComponentFactory<any>;
  questionModule: QuestionModuleComponent;
  lastQuestion: boolean;
  lastModule: boolean;
  submitSend: boolean;
  submitCorrect: boolean;
  correctFeedback: string;
  wrongFeedback: string;
  feedbackIterator = 0;
  progress: Array<Array<string>>
  allQuestionsInCourse: number
  submitResponse = {};

  dashboard = false;
  private ngUnsubscribe: Subject<void> = new Subject<void>(); // = new Subject(); in Typescript 2.2-2.4

  constructor(
    private translate: TranslateService,
    private router: Router,
    public server: ServerService,
    private route: ActivatedRoute,
    private factory: ComponentFactoryResolver,
    public dialog: MdDialog
  ) {
    this.loadQuestion()
  }

  ngOnInit() {
  }

  ngOnDestroy() {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }

  loadQuestion() {
    this.route.params.subscribe((data: Params) => {
      this.courseID = Number(data.id);
      this.moduleIndex = Number(data.module);
      this.questionIndex = data.question;
      this.server.get(
        'courses/' + this.courseID + '/' + (
          Number(this.moduleIndex) - 1
        ) + '/' + (Number(this.questionIndex) - 1 ))
        .then(response => {
        this.setupQuestion(response)
      })
    })
  }

  setupQuestion(data) {
    this.submitCorrect = false;
    this.title = data['title']
    this.questionBody = data['text']
    this.lastQuestion = data['last_question']
    this.lastModule = data['last_module']
    this.learning_text = data['learning_text']
    this.progress = data['progress']
    this.allQuestionsInCourse = 0;
    for (let i = 0; i < this.progress.length; i++) {
      this.allQuestionsInCourse += this.progress[i].length
    }

    // create Question based on the class
    this.questionFactory = this.factory.resolveComponentFactory(this.components[data['type']])

    // empty question factory box bevor adding new stuff
    if (this.question.length > 0) {
      this.question.clear()

    }
    // load the current question Type on the screen
    const question = this.question.createComponent(this.questionFactory)
    this.questionModule = (<QuestionModuleComponent> question.instance)
    // give the question its data
    this.questionModule.data = data['question_body']
  }


  submit() {
    const postData = {answers: this.questionModule.submit()};
    this.server.post(
      'courses/' + this.courseID + '/' + (
        Number(this.moduleIndex) - 1
      ) + '/' + (Number(this.questionIndex) - 1),
      postData)
      .then(data => this.evaluteAnswer(data))
      .catch(err => console.log(err))
  }

  evaluteAnswer(data) {

    this.submitResponse = data
    this.submitCorrect = data['evaluate']
    this.submitSend = true;

    if (this.submitCorrect) {
      // calls block to freeze the question element
      this.questionModule.block();
      this.questionModule.feedback = data.custom_feedback

      this.progress[this.moduleIndex - 1][this.questionIndex - 1]['solved'] = true
      // the answer is correct and the correct Feedback will be set
      if (data['feedback'] !== '') {
        this.correctFeedback = data['feedback']
      } else {
        this.translate.get('correct feedback').subscribe(translated => {
          this.correctFeedback = translated
        })
      }
    } else {
      this.feedbackIterator = (this.feedbackIterator + 1) % 3;
      // answer was wrong and the wrong Feedback will be setup
      let text = '';
      this.translate.get('wrong feedback ' + this.feedbackIterator).subscribe(translated => {
        text = translated
      })
      console.log(WrongFeedbackComponent)
      const wrongFeedback = this.dialog.open(WrongFeedbackComponent, {
        data: { text: text }
      })
      console.log(wrongFeedback)
    }
  }

  next() {
    // if this is not the last question of a module add 1 to the index
    if (this.submitResponse['next'] === 'question') {
      this.questionIndex++;
    } else if (this.submitResponse['next'] === 'module') {
      // if this is the last Question but not the last module add one to module and start the question counter at 1
      this.moduleIndex++;
      this.questionIndex = 1;
    } else if (this.submitResponse['next'] === 'quiz') {
      this.router.navigateByUrl('/course/' + this.courseID + '/quiz')
      return
    } else {
      // TODO add a feedback for the course here
      this.router.navigateByUrl('/course')
      return;
    }
    this.router.navigateByUrl('/course/' + this.courseID + '/' + this.moduleIndex + '/' + this.questionIndex)
    this.submitSend = false;
    this.loadQuestion()
  }

}
