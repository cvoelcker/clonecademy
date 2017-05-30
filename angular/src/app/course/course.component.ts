import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router'
import { ServerService } from '../service/server.service'

@Component({
  selector: 'app-course',
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.css']
})
export class CourseComponent implements OnInit {

  id: number;
  type: string;
  name: string;
  modules: [any];

  constructor(private route: ActivatedRoute, private server: ServerService) {

  }

  ngOnInit() {
    this.route.params.subscribe((data: Params) => {this.id = data.id})
    this.server.get('courses/'+this.id + "/")
      .then(data => {
        this.name = data.name;
        this.modules = data.modules;
      })

  }

}
