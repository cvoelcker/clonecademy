import { Component, OnInit, ViewChild, ViewContainerRef} from '@angular/core';

import { CourseService } from '../service/course.service'
import { UserService } from '../service/user.service'

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

  @ViewChild('content', {read: ViewContainerRef}) content: ViewContainerRef;

  constructor(private course: CourseService, private user: UserService) {

  }

  ngOnInit() {
    this.course.load().then(() => this.loading = false)
  }

}
