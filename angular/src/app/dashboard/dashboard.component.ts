import { Component, OnInit,} from '@angular/core';

import { CourseService } from '../service/course.service'

import { trigger, state, style, animate, transition } from '@angular/animations';


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
  data: any;
  collapse: boolean

  loading = true;


  constructor(private course: CourseService) {

  }

  ngOnInit() {
    this.course.load().then(() => this.loading = false)
  }

}
