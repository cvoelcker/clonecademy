import {Component, OnInit, Input} from '@angular/core';

import {ActivatedRoute, Params, Router} from '@angular/router'

import {ServerService} from '../../../service/server.service'

import 'rxjs/Rx' ;

/**
 * @author Leonhard Wiedmann
 *
 * A component to display the statistics of the current course
 */
@Component({
  selector: 'app-course-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.scss']
})
export class CourseStatisticsComponent implements OnInit {

  id: number;
  list: any;

  // Pie variables
  loadingPie = false;
  pieChartLabels  = ['Solved', 'Not solved'];
  pieChartData = [];
  pieChartColor = [{ backgroundColor: [ '#aaff80' , 'darkred' ]}];

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

  /**
  Load the variables for the pie view
  @author Leonhard Wiedmann
  **/
  loadPie() {
    this.loadingPie = true;
    this.server.post('statistics', {
      course: this.id,
      filter: 'solved'
    }).then((data: any) => {
        this.pieChartData = [data['True'], data['False']]
        this.loadingPie = true;
      })
  }

  /**
  Load the list of questions, how many tries this question has and how many correct tries it has
  @author Leonhard Wiedmann
  **/
  loadList() {
    this.loadingPie = true;
    this.server.post('statistics', {
      list_questions: true,
      course: this.id,
    }).then((data: any) => {
        this.list = data
      })
  }

  /**
  Download the statistics for the current user
  @author Leonhard Wiedmann
  **/
  downloadStatistics() {
    this.server.downloadStatistics({id: 0})
  }

}
