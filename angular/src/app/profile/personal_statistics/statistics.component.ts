import {Component, OnInit, Input} from '@angular/core';

import {ServerService} from '../../service/server.service'
import {UserService} from '../../service/user.service'

import 'rxjs/Rx' ;

/**
 * @author Leonhard Wiedmann
 *
 * A component to display the statistics of the current user
 */

@Component({
  selector: 'app-personal-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.scss']
})
export class StatisticsComponent implements OnInit {
  statistics= [
    {day: 'Sunday', stat: [] },
    {day: 'Monday', stat: [] },
    {day: 'Tuesday', stat: [] },
    {day: 'Wednesday', stat: [] },
    {day: 'Thursday', stat: [] },
    {day: 'Friday', stat: [] },
    {day: 'Saturday', stat: [] }
  ];
  monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  height = 0;
  loading = true
  currentDate: any
  offsetEnd: Date;
  offsetDate: Date;
  previousWeek = 0;
  loadStats = true;

  // Pie variables
  pieChartLabels = [];
  pieChartData = [];
  pieChartColor = [ {backgroundColor: [] } ];
  totalQuestion = 0;
  loadedPie: boolean;

  constructor(private user: UserService, private server: ServerService) {
    this.currentDate = new Date();
    this.offsetDate = new Date();
    this.offsetDate.setDate(this.currentDate.getDate() - 7)
    // rearange the days array for the current day
    for(let i = this.statistics.length - 1; i > this.offsetDate.getDay(); i--){
      const day = Object.assign(this.statistics[i])
      this.statistics.splice(i, 1);
      this.statistics.unshift(day)
    }
  }

  ngOnInit() {
    this.loadDate()
    this.loadPie()
  }

  /***
  count the number of solved questions of this array
  @author Leonhard Wiedmann
  ***/
  solvedQuestions(data: Array<any>) {
    let counter = 0;
    for (let i = 0; i < data.length; i++) {
      if (data[i]['solved']) {
        counter = counter + 1;
      }
      return counter
    }
  }

  /**
  Load the data for the Pie view
  This function is edition only pie variables

  @author Leonhard Wiedmann
  **/
  loadPie() {
    this.loadedPie = false;
    this.server.post('statistics', {
      id: this.user.id,
      solved: true,
      categories__with__counter: true}).then((data: Array<{name: string, color: string, counter: number}>) => {
        this.totalQuestion = 0;
        for (let i = 0; i < data.length; i++) {
          this.totalQuestion += data[i].counter;
          this.pieChartLabels.push(data[i].name)
          this.pieChartData.push(data[i].counter)
          this.pieChartColor[0].backgroundColor.push(data[i].color)
        }
        this.loadedPie = true;

      })
  }

  /**
  Load the data for the weekly statistics
  first calculate the week, then load the data from the server and set it
  the week is calculated by the offsetDate + 7 days
  @author Leonhard Wiedmann
  **/
  loadDate() {
    this.loadStats = true;
    for ( let i = 0 ; i < this.statistics.length; i++) {
      this.statistics[i].stat = []
    }
    const startDate = this.offsetDate.getFullYear() + '-' + (
      this.offsetDate.getMonth() + 1
    ) + '-' + Number(this.offsetDate.getDate() + 1) + ' 00:00:00'
    this.offsetEnd = new Date( this.offsetDate.getTime() + 7 * 24 * 60 * 60 * 1000 )
    const endDate = this.offsetEnd.getFullYear() + '-' + (this.offsetEnd.getMonth() + 1) + '-' + this.offsetEnd.getDate() + ' 23:59:59'
    this.server.post('statistics',
    {
      id: this.user.id,
      order: 'question__module__course__category',
      date: { end: endDate, start: startDate },
      serialize: [
        'question__module__course__category__color',
        'question__module__course__category__name',
        'quiz_question__course__category__color',
        'quiz_question__course__category__name',
        'solved'
      ]
    } , true)
      .then((data: any) => {
        for (let j = 0; j < 7; j ++){
          const tmpDate = new Date();
          tmpDate.setDate(this.currentDate.getDate() - j)
          for (let i = 0; i < data.length; i++) {
            const s = data[i]
            const day = (Number(data[i]['date'].split('/')[0]))
            if (tmpDate.getDay() === day) {
              this.statistics[6 - j ]['stat'].push(data[i])
            }
          }
        }
        // calculate the height variable for the % height of the bars
        this.height = this.statistics[0].stat.length

        // count the number of questions for the height of the bars
        // the height of the bars will be calculated by (number_of_quesions / this.height)
        for ( let i = 0 ; i < this.statistics.length ; i++ ) {
          this.statistics[i].stat['solved'] = 0;
          for (let j = 0; j < this.statistics[i].stat.length; j++) {
            if ( this.statistics[ i ].stat[ j ].solved ) {
              this.statistics[i].stat['solved'] += 1;
            }
          }
          if ( this.height < this.statistics[ i ].stat.length ) {
            this.height = this.statistics[i].stat.length
          }
        }
        this.loading = false;
        this.loadStats = false;
      })
      .catch(err => {
        this.loading = false;
      })
  }

  downloadStatistics() {
    this.server.downloadStatistics({id: this.user.id})
  }

}
