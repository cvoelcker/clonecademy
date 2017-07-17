import { Component, OnInit } from '@angular/core';

import {CookieService} from 'angular2-cookie/core';

import { UserService } from '../service/user.service'

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})
export class MenuComponent implements OnInit {

  login: boolean;

  constructor(private cookie: CookieService, private user: UserService){
    this.login = this.cookie.get("token") != null
  }

  ngOnInit() {
  }

}
