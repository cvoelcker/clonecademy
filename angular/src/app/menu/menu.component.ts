import { Component, OnInit } from '@angular/core';

import {CookieService} from 'angular2-cookie/core';

import { UserService } from '../service/user.service'

import { Http} from '@angular/http';



@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})

export class MenuComponent implements OnInit {

  links: Array<{url: string, name: string}> = [
    {url: "about", name: "About"},
    {url: 'impressum', name: "Impressum"},
  ]
  login: boolean;

  constructor(private cookie: CookieService, private user: UserService, public http: Http){
    this.login = this.cookie.get("token") != null
  }

  ngOnInit() {
  }

}
