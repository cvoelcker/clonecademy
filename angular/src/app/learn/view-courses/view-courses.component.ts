import { Component, OnInit, ViewChild, ViewContainerRef} from '@angular/core';

import { CourseService } from '../../service/course.service'
import { UserService } from '../../service/user.service'

import { trigger, state, style, animate, transition } from '@angular/animations';

@Component({
  selector: 'app-view-course',
  templateUrl: './view-courses.component.html',
  styleUrls: ['./view-courses.component.scss'],
  animations: []
})

export class CourseViewComponent{
  data: any;

  loading = true;
  loadingCat = true;
  courses = [];

  ngAfterViewInit(){
    this.loading = true;
    this.loadingCat = true;
    this.course.load().then(() => {
      this.loading = false,
      this.loadingCat = false,
      this.courses = this.course.get_started()
    })
  }

  constructor(private course: CourseService, private user: UserService) {
  }


}
