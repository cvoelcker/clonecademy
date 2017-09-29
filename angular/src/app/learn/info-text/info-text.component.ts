import {Component, OnInit, Input} from '@angular/core';

import {QuestionModuleComponent} from '../question/question.module'
import {ServerService} from '../../service/server.service'

/**
To create and edit a info type question
@author Claas Völcker
**/
@Component({
  selector: 'app-information-text',
  templateUrl: './info-text.component.html',
  styleUrls: ['./info-text.component.scss']
})
export class InformationTextComponent extends QuestionModuleComponent {

  /**
    return array of the marked answers
    @author Class Völcker
  **/
  submit(): any {
    return true;
  }
}
