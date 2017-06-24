import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router'
import { ServerService } from '../service/server.service'
import { CourseService } from '../service/course.service'
@Component({
  selector: 'app-course',
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.scss']
})
export class CourseComponent implements OnInit {

  id: number;
  type: string;
  name: string;
  modules: [any];
  solved: [number, number];
  completed: boolean = true;
  loading = true;


  constructor(
    private course: CourseService,
    private route: ActivatedRoute,
    private server: ServerService,
    private router: Router,
  ) {

  }

  ngOnInit(){
    this.route.params.subscribe(data => {
      this.id = data.id
      this.load();
    })
  }

  load() {
    this.course.contains(this.id).then(() => {
      this.server.get('courses/'+this.id + "/", true)
      .then(data => {
        this.name = data['name'];
        this.modules = data['modules'];
        this.solved = data['solved'];
        console.log(this.solved)

        let lastModule = this.modules[this.modules.length - 1]
        let lastQuestion = lastModule.question[lastModule.question.length - 1]
        if(!(data['solved'].indexOf(lastQuestion.id) > -1)){
          this.completed = false;
        }
        this.loading = false
      })
    })
    .catch(() => {

      this.router.navigate(["/course/page_not_found"])
    })
  }



}
