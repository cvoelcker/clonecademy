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
  completed: boolean = false;
  loading = true;
  lastCourse = [1, 1];
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
      // save the number of answered questions and the amount of questions in the current course


      this.completed = false;
      this.loading = true;
      this.modules = undefined;
      this.name = "";
      // send request to server to get the information for the course
      this.server.get('courses/'+this.id + "/", true, false)
      .then(data => {
        this.numQuestions = data['num_questions']
        this.numAnswered = data['num_answered']
        this.pieChartData = [this.numAnswered, this.numQuestions-this.numAnswered]
        this.name = data['name'];
        this.modules = data['modules'];

        let lastModule = this.modules[this.modules.length - 1]
        if(lastModule != undefined){

          let lastQuestion = lastModule.questions[lastModule.questions.length - 1]
          if(lastQuestion.solved == true){
            this.completed = true;
          }
        }
        else {
          this.completed = true;
        }
        if(!this.completed){
          for(let i = 0; i < this.modules.length; i++){
            for(let j = 0; j < this.modules[i].questions.length; j++){
              if(this.modules[i].questions[j].solved){
                this.lastCourse = [i+1, j+1];
              }
            }
          }
        }
        this.loading = false
      })
    .catch((error) => {

      this.router.navigate(["/course/page_not_found"])
    })
  }






}
