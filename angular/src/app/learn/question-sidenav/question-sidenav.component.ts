import {Component, OnInit, Input, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {MdListModule} from '@angular/material';
import {ServerService} from '../../service/server.service';
import {CourseService} from '../../service/course.service';

@Component({
  selector: 'app-question-sidenav',
  templateUrl: './question-sidenav.component.html',
  styleUrls: ['./question-sidenav.component.scss']
})
export class QuestionSidenavComponent implements OnInit {

  id: number;
  type: string;
  name: string;
  description: string;
  modules: [any];
  completed: boolean = false;
  loading = true;
  lastCourse = [1, 1];
  numAnswered: number;
  numQuestions: number;
  @Input() sidemenu: any;

  public chartHovered(e: any): void {
  }

  constructor(private course: CourseService,
              private route: ActivatedRoute,
              private server: ServerService,
              private router: Router,) {

  }

  closeSidemenu() {
    if (this.sidemenu) {
      this.sidemenu.close()
    }
  }

  ngOnInit() {
    //this.initChart()
    this.route.params.subscribe(data => {
      this.id = data.id
      this.load(data.id);
    })
  }

  load(id: number) {
    // save the number of answered questions and the amount of questions in the current course
    this.completed = false;
    this.loading = true;
    this.modules = undefined;
    this.name = '';
    // send request to server to get the information for the course
    this.server.get('courses/' + id + '/', true, false)
      .then(data => {
        this.numQuestions = data['num_questions']
        this.numAnswered = data['num_answered']
        this.name = data['name'];
        this.description = data['description']
        this.modules = data['modules'];
        //this.pieChartData = [this.numAnswered, this.numQuestions-this.numAnswered]

        let lastModule = this.modules[this.modules.length - 1]
        if (lastModule != undefined) {

          let lastQuestion = lastModule.questions[lastModule.questions.length - 1]
          if (lastQuestion.solved == true) {
            this.completed = true;
          }
        }
        else {
          this.completed = true;
        }
        if (!this.completed) {
          for (let i = 0; i < this.modules.length; i++) {
            for (let j = 0; j < this.modules[i].questions.length; j++) {
              if (this.modules[i].questions[j].solved) {
                this.lastCourse = [i + 1, j + 1];
              }
            }
          }
        }
        this.loading = false
      })
      .catch((error) => {

        this.router.navigate(['/course/page_not_found'])
      })
  }
}
