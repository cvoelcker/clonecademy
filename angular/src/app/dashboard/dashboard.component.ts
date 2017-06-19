import { Component, OnInit, ViewChild, ViewContainerRef} from '@angular/core';

import { CourseService } from '../service/course.service'
import { UserService } from '../service/user.service'

import { trigger, state, style, animate, transition } from '@angular/animations';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  animations: [
      trigger('slideIn', [
          state('1', style({ "height": "*", 'overflow-y': 'hidden' })),
          state('0', style({ "height": "0",  'overflow-y': 'hidden' })),
          transition('1 => 0', [
              style({ height: '*' }),
              animate(250, style({ height: 0 }))
          ]),
          transition('0 => 1', [
              style({ height: '0' }),
              animate(250, style({ height: '*' })),
      ]),
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
