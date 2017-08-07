import { Component, OnInit, Input } from '@angular/core';

import { QuestionModule } from "../question/question.module"
import { ServerService } from "../../service/server.service"

@Component({
  selector: 'app-InformationText',
  templateUrl: './info-text.component.html',
  styleUrls: ['./info-text.component.scss']
})
export class InformationTextComponent extends QuestionModule {

  data = {}

  // return array of the marked answers
  submit(): any{
    return this.data;
  }
}
