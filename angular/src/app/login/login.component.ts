import { Component, OnInit } from '@angular/core';

import { UserService } from '../service/user.service';
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

  constructor(private cookie: CookieService, private user: UserService, private router: Router) {

  }

  login(){
    this.user.login(this.username, this.password)
      .then(res => {this.router.navigate(['/dashboard'])})
      .catch(res => {this.invalidLogin = true;})
  }
  ngOnInit() {
    if(this.cookie.get('token') != null){
      this.router.navigate(['/dashboard']);
    }
  }

}
