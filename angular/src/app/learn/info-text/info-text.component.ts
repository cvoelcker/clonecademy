import {Component, OnInit, Input} from '@angular/core';

import {QuestionModuleComponent} from '../question/question.module'
import {ServerService} from '../../service/server.service'

@Component({
  selector: 'app-information-text',
  templateUrl: './info-text.component.html',
  styleUrls: ['./info-text.component.scss']
})
export class InformationTextComponent extends QuestionModuleComponent {

  // return array of the marked answers
  submit(): any {
    return true;
  }
}
