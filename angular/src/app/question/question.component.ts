import { Component, OnInit, Input } from '@angular/core';
import { ServerService } from "../service/server.service"


@Component({
  selector: 'app-question',
  templateUrl: './question.component.html',
  styleUrls: ['./question.component.css']
})
export class QuestionComponent implements OnInit {

  @Input() data: any;
  moduleIndex: number;
  courseID: number;

  constructor(public server: ServerService) { }

  ngOnInit() {
  }

  submit(): Promise<boolean>{
    return new Promise<boolean>((resolve, reject) => {reject(false)})
  }

}
