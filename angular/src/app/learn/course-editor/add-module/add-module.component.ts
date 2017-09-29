import {
  Component,
  ChangeDetectorRef,
  Type,
  OnInit,
  Output,
  EventEmitter,
  ViewChild,
  ViewContainerRef,
  ComponentFactoryResolver,
  ComponentFactory,
  AfterViewInit
} from '@angular/core';

import {AddQuestionComponent} from '../add-question/add-question.component'

import {slideIn} from '../../../animations';

import {AddQuestionModuleComponent} from '../add-question/add-question.module'
import {QuestionDictionary} from '../../question-dictionary';

import {trigger, state, style, animate, transition} from '@angular/animations';


@Component({
  selector: 'app-add-module',
  templateUrl: './add-module.component.html',
  styleUrls: ['./add-module.component.scss'],
  animations: [slideIn]
})
export class AddModuleComponent implements AfterViewInit {

  components: Array<{ name: string, key: string, component: Type<AddQuestionModuleComponent> }> = QuestionDictionary.detailComponents;
  selectedValue: Type<AddQuestionComponent> = null;
  title = '';
  learningText = '';
  selected: boolean;
  question: ComponentFactory<AddQuestionComponent>;
  questionArray = [];
  moduleComponent: AddQuestionComponent;
  id: number;
  collapse: boolean;

  // the parent class set this to true when the save button is pressed
  form = null;

  loading = false;

  @ViewChild('module', {read: ViewContainerRef}) module: ViewContainerRef;

  @Output() clear: EventEmitter<any> = new EventEmitter();

  constructor(private ref: ChangeDetectorRef, private factory: ComponentFactoryResolver) {
    this.question = this.factory.resolveComponentFactory(AddQuestionComponent)
  }


  addQuestion(component, data) {
    // add the question to the module component and add it to the array so we can edit and save it later
    const question = this.module.createComponent(this.question)
    const q = (<AddQuestionComponent> question.instance)
    q.form = this.form

    q.emitter.subscribe(stuff => this.module.detach())
    q.child = component
    q.addQuestion(data)
    this.questionArray.push(question)
    this.selectedValue = null;

  }

  editQuestion(data) {
    let cmp: Type<AddQuestionModuleComponent> = null;
    for (let i = 0; i < this.components.length; i++) {
      if (data['type'] === this.components[i].key) {
        cmp = this.components[i].component
        break;
      }
    }

    this.addQuestion(cmp, data)
  }

  ngAfterViewInit() {
    this.loading = true;
    this.ref.detectChanges()
  }

  // emit remove so parent class can remove this
  close() {
    this.loading = false;
    // this.clear.emit('remove')
  }

  remove(event) {
    if (event.toState === '0' && this.loading === false) {
      this.clear.emit('remove')
    }
  }

  // emit up so parent class can change the position
  up() {
    this.clear.emit('up')
  }

  // emit down so parent can change the position
  down() {
    this.clear.emit('down')
  }


  // save all questions in the correct order
  // append title, and the module description and return it
  save(form) {
    this.form = form;
    const values = [];
    for (let i = 0; i < this.questionArray.length; i++) {
      const tmp = this.questionArray[i];
      const index = this.module.indexOf(this.questionArray[i].hostView)
      if (index >= 0) {
        const save = (<AddQuestionComponent> tmp.instance).save(form)
        save['order'] = index;
        values.push(save)
      }
    }

    return {
      name: this.title,
      questions: values,
      id: this.id,
      learning_text: this.learningText
    };
  }

}
