import {Component, OnInit, Input} from '@angular/core';

import {Http, RequestOptions, Headers} from '@angular/http';

import {CookieService} from 'angular2-cookie/core';
import {ServerService} from '../../service/server.service'
import {UserService} from '../../service/user.service'

import 'rxjs/Rx' ;

@Component({
  selector: 'app-ranking-list',
  templateUrl: './ranking-list.component.html',
  styleUrls: ['./ranking-list.component.scss']
})
/**
 * @author Claas Voelcker
 *
 * A component to display a ranking of all users
 */
export class RankingListComponent implements OnInit {
  profiles: {};
  loading = true

  constructor(private user: UserService, private server: ServerService) {
  }

  ngOnInit() {
    this.server.get('ranking', true, false)
      .then(data => {
        this.profiles = data;
        this.loading = false;
      })
      .catch(err => {
        this.loading = false;
      })
  }
}
