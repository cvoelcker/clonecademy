import { Component, OnInit, Input } from '@angular/core';

import { Http, RequestOptions, Headers } from '@angular/http';

import {CookieService} from 'angular2-cookie/core';
import { ServerService } from '../../service/server.service'
import { UserService } from '../../service/user.service'

import 'rxjs/Rx' ;

@Component({
  selector: 'statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.scss']
})
export class StatisticsComponent implements OnInit {
  statistics: {};
  loading = true

  constructor(private user: UserService, private server: ServerService, private cookie: CookieService, private http: Http) {
  }

  ngOnInit() {
    this.server.get("user/statistics", true, false)
      .then(data => {
        this.statistics = data;
        for(let s in this.statistics){
          s["date"] = new Date(s["date"]);
        }
        this.loading = false;
      })
        .catch(err => {
        this.loading = false;
      })
  }

  downloadStatistics(){
    this.server.downloadStatistics({id: this.user.id})
  }

}
