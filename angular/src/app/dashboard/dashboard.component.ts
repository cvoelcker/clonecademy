import { Component, Type, OnInit, Output, EventEmitter, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory } from '@angular/core';

import { ServerService} from '../service/server.service'

import { trigger, state, style, animate, transition } from '@angular/animations';

import { CourseComponent } from '../course/course.component'

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
  data: any;
  create: boolean;
  statistics: boolean;
  collapse: boolean

  course: ComponentFactory<CourseComponent>;
  addCourse: ComponentFactory<CreateCourseComponent>;

  @ViewChild('details', {read: ViewContainerRef}) details: ViewContainerRef;

  constructor(private server: ServerService, private factory: ComponentFactoryResolver) {
    this.course = this.factory.resolveComponentFactory(CourseComponent)
    this.addCourse = this.factory.resolveComponentFactory(CreateCourseComponent)

  }

  ngOnInit() {
    this.create = false;
    this.statistics = false;

    this.server.get("courses/")
      .then(data => {
        this.data = data
      }
      )
      .catch(err => console.log(err))
  }

  createClicked(){
    this.details.clear()
    this.details.createComponent(this.addCourse)
  }

  courseClicked(id: number){
    this.details.clear()
    let courseView = this.details.createComponent(this.course)
    let course = (<CourseComponent> courseView.instance)
    course.id = id;
    course.load()
  }

}
