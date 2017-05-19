import { Component, OnInit } from '@angular/core';

import { ServerService } from '../service/server.service';
import { Router } from "@angular/router"

import { CookieService } from 'angular2-cookie/core';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  username: string
  password: string;
  submitted: boolean;
  invalidLogin: boolean;

  constructor(private cookie: CookieService, private server: ServerService, private router: Router) {

  }

  login(){
    this.server.login(this.username, this.password)
      .then(res => {this.router.navigate(['/dashboard'])})
      .catch(res => {this.invalidLogin = true;})
  }
  ngOnInit() {
    if(this.cookie.get('token') != null){
      this.router.navigate(['/dashboard']);
    }
  }

}
