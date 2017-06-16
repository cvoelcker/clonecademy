import { Component, OnInit } from '@angular/core';

import { trigger, state, style, animate, transition } from '@angular/animations';

import { UserService } from '../service/user.service';
import { Router } from "@angular/router";
import { ServerService } from '../service/server.service'

import { CookieService } from 'angular2-cookie/core';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  animations: [
    trigger('show', [
      state( "active", style({
        display: "none"
      })),
      state( "inactive", style({
        display: "block"
      })),
      transition('inactive => active', animate('100ms ease-in')),
    ])
  ]
})
export class LoginComponent implements OnInit {

  username: string
  password: string;
  submitted: boolean;
  invalidLogin: boolean;

  constructor(private cookie: CookieService,public server: ServerService, public user: UserService, private router: Router) {

  }

  login(){
    this.user.loginUser(this.username, this.password)
  }

  ngOnInit() {
    if(this.cookie.get('token') != null){
      this.router.navigate(['/dashboard']);
    }
  }

}
