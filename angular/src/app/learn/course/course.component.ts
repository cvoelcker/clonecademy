import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router'
import { ServerService } from '../../service/server.service'
import { CourseService } from '../../service/course.service'
import { SassHelperComponent } from '../../service/sass-helper/sass-helper'
@Component({
  selector: 'app-course',
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.scss']
})
export class CourseComponent implements OnInit {

  @ViewChild(SassHelperComponent) private sassHelper: SassHelperComponent;

  id: number;
  type: string;
  name: string;
  modules: [any];
  solved: [number, number];
  completed: boolean = true;
  loading = true;
  numAnswered: number;
  numQuestions: number;

  //Pie
  public pieChartLabels:string[] = ['answered', 'to do'];
  public pieChartData:number[];
  public pieChartType:string = 'pie';
  public pieChartColor:any;

  // events
public chartHovered(e:any):void {
}


  constructor(
    private course: CourseService,
    private route: ActivatedRoute,
    private server: ServerService,
    private router: Router,
  ) {

  }

  initChart(){
    this.pieChartColor = [
      {
        backgroundColor: [
          this.sassHelper.readProperty('success'),
          this.sassHelper.readProperty('warning'),
        ],
        strokeColor: '#0f0',
        hoverBackgroundColor: [
          this.sassHelper.readProperty('success-hover'),
          this.sassHelper.readProperty('warning-hover'),
        ],
        borderColor: "transparent"
      },
    ]
  }

  ngOnInit(){
    this.initChart()
    this.route.params.subscribe(data => {
      this.id = data.id
      this.load();
    })
  }

  load() {
    this.course.contains(this.id).then((data) => {
      // save the number of answered questions and the amount of questions in the current course
      this.numQuestions = data['num_questions']
      this.numAnswered = data['num_answered']
      this.pieChartData = [this.numAnswered, this.numQuestions-this.numAnswered]

      // send request to server to get the information for the course
      this.server.get('courses/'+this.id + "/", true)
      .then(data => {
        this.name = data['name'];
        this.modules = data['modules'];
        this.solved = data['solved'];

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
