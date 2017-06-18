import { Component, Type, OnInit, Output, EventEmitter, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory } from '@angular/core';

import { ServerService} from '../service/server.service'

import { trigger, state, style, animate, transition } from '@angular/animations';

import { CourseComponent } from '../course/course.component'

import { ActivatedRoute, Params, Router } from '@angular/router'

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
  collapse: boolean

  course: ComponentFactory<CourseComponent>;
  addCourse: ComponentFactory<CreateCourseComponent>;
  loading = true;

  @ViewChild('details', {read: ViewContainerRef}) details: ViewContainerRef;

  constructor(private server: ServerService, private factory: ComponentFactoryResolver, private route: ActivatedRoute, private router: Router) {
    // create factories for later use
    this.course = this.factory.resolveComponentFactory(CourseComponent)
    this.addCourse = this.factory.resolveComponentFactory(CreateCourseComponent)

  }

  ngOnInit() {

    // check if subpage is opend
    this.route.params.subscribe((data: Params) => {
      if(data.id != null){
        this.courseClicked(data.id)

      }
    })
    // load the list of courses from the server
    this.server.get("courses/", true)
      .then(data => {
        this.data = data
        this.loading = false;
        }
      )

  }

  // to set the basic view when user enters dashboard
  baseDashboard(){
    this.details.clear()
  }

  // show module create Course and handel what happens when user click save
  createClicked(){
    this.details.clear()
    let component = this.details.createComponent(this.addCourse)

    let module = (<CreateCourseComponent> component.instance)
    module.emitter.subscribe(data => {
      this.baseDashboard()
    })
  }

  // open the course details in the content Window
  // it shows the learning Text and the questions
  courseClicked(id: number){
    this.details.clear()
    this.router.navigate(['/course/' + id])
    let courseView = this.details.createComponent(this.course)
    let course = (<CourseComponent> courseView.instance)
    course.id = id;
    course.load()
  }

}
