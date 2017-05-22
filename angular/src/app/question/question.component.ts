import { Component, OnInit, Input } from '@angular/core';


@Component({
  selector: 'app-question',
  templateUrl: './question.component.html',
  styleUrls: ['./question.component.css']
})
export class QuestionComponent implements OnInit {

  @Input() data: any;
  moduleID: number;
  courseID: number;

  constructor() { }

  ngOnInit() {
  }

}
