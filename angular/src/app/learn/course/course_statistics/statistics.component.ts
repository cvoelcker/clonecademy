import {Component, OnInit, Input} from '@angular/core';

import {ActivatedRoute, Params, Router} from '@angular/router'

import {ServerService} from '../../../service/server.service'

import 'rxjs/Rx' ;

@Component({
  selector: 'CourseStatistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.scss']
})
export class CourseStatisticsComponent implements OnInit {

  id: number;
  list: any;

  constructor(
    private server: ServerService,
    private route: ActivatedRoute,
  ) {

  }

  ngOnInit() {
    this.route.params.subscribe(data => {
      this.id = data.id
    })
    this.loadPie()
    this.loadList()
  }

  //Pie
  loadingPie = false;
  public pieChartLabels:string[] = ["Solved", "Not solved"];
  public pieChartData:number[]= [];
  public pieChartColor:any = [{backgroundColor: ["#7cf700", "#d4043b"]}];

  loadPie(){
    this.loadingPie = true;
    this.server.post("statistics", {
      course: this.id,
      filter: "solved"
    }).then((data: any) => {
        this.pieChartData = [data['True'], data['False']]
        this.loadingPie = true;
      })
  }

  loadList(){
    this.loadingPie = true;
    this.server.post("statistics", {
      list_questions: true,
      course: this.id,
    }).then((data: any) => {
        this.list = data
      })
  }

  downloadStatistics() {
    this.server.downloadStatistics({id: 0})
  }

}
