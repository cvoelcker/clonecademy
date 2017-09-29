import {Component, OnInit, Input, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router'
import {ServerService} from '../../service/server.service'
import {CourseService} from '../../service/course.service'
import {UserService} from '../../service/user.service'


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
  completed = false;
  loading = true;
  lastCourse = [1, 1];
  numAnswered: number;
  numQuestions: number;
  description: string;
  visible: boolean;
  @Input() sidemenu: any;
  quiz: boolean;

  // Pie
  // public pieChartLabels:string[] = ['answered', 'to do'];
  // public pieChartData:number[];
  // public pieChartType:string = 'pie';
  // public pieChartColor:any;

  // events
  public chartHovered(e: any): void {
  }

  constructor(private course: CourseService,
              private route: ActivatedRoute,
              private server: ServerService,
              private router: Router,
              private user: UserService) {

  }

  closeSidemenu() {
    if (this.sidemenu) {
      this.sidemenu.close()
    }
  }

  //
  // initChart(){
  //   this.pieChartColor = [
  //     {
  //       backgroundColor: [
  //         this.sassHelper.readProperty('success'),
  //         "white"
  //       ],
  //       strokeColor: '#0f0',
  //       hoverBackgroundColor: [
  //         this.sassHelper.readProperty('success-hover'),
  //         "white"
  //       ],
  //       borderColor: "transparent"
  //     },
  //   ]
  // }

  ngOnInit() {
    // this.initChart()
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
        this.modules = data['modules'];
        this.description = data['description']
        this.visible = data['is_visible']
        this.quiz = data['quiz']
        // this.pieChartData = [this.numAnswered, this.numQuestions-this.numAnswered]

        const lastModule = this.modules[this.modules.length - 1]
        if (lastModule !== undefined) {

          const lastQuestion = lastModule.questions[lastModule.questions.length - 1]
          if (lastQuestion.solved === true) {
            this.completed = true;
          }
        } else {
          this.completed = true;
        }
        if (!this.completed) {
          for (let i = 0; i < this.modules.length; i++) {
            for (let j = 0; j < this.modules[i].questions.length; j++) {
              if (this.modules[i].questions[j].solved) {
                if ( j  == this.modules[i].questions.length - 1){
                  this.lastCourse = [i + 2, 0];
                }
                else{
                  this.lastCourse = [i + 1, j + 1];

                }
              }
            }
          }
        }
        this.loading = false
      })
      .catch((error) => {
        console.log(error)
        this.router.navigate(['/course/page_not_found'])
      })
  }

  /*
  this function toggles the visibility of the current course
  it is called by the visibility button
  @author Tobias Huber
  */
  toggleVisibility() {
    this.server.post('courses/' + this.id + '/toggleVisibility', {})
      .then(answer => {
        this.visible = answer['is_visible']
      })
  }
}
