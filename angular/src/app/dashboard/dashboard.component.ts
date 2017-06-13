import { Component, OnInit } from '@angular/core';

import { ServerService} from '../service/server.service'

import { trigger, state, style, animate, transition } from '@angular/animations';


import { CreateCourseComponent } from '../create-course/create-course.component'

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  animations: [
    trigger('show', [
      state( "active", style({
        display: "none"
      })),
      state( "inactive", style({
        display: "block"
      })),
      transition('inactive => active', animate('100ms ease-in')),
    ])
  ]
})
export class DashboardComponent implements OnInit {
  course: any;
  create: boolean;
  statistics: boolean;
  collapse: boolean

  constructor(private server: ServerService) {

  }

  ngOnInit() {
    this.create = false;
    this.statistics = false;

    this.server.get("courses/")
      .then(data => {
        this.course = data
      }
      )
      .catch(err => console.log(err))
  }

  createclicked(){
    this.create = true;
    this.statistics = false;

  }

  statisticsclicked(){
    this.statistics = true;
    this.create = false;
  }


}
