import { Component, OnInit } from '@angular/core';

import { trigger, state, style, animate, transition } from '@angular/animations';

import { ServerService } from '../service/server.service';
import { Router } from "@angular/router"

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

  /*
  variables for register
  TODO: refactor name and surname to first and last name
   */
  newUsername: string;
  newEmail: string;
  newPassword: string;
  newPassword2: string;
  newFirstName: string = "";
  newLastName: string = "";
  newAge: number = -1;
  newGroup: string = "";
  invalidRegister: boolean;
  errorMessage: string;

  showLogin = true;



  constructor(private cookie: CookieService, private server: ServerService, private router: Router) {

  }

  login(){
    this.server.login(this.username, this.password)
      .then(res => {this.router.navigate(['/dashboard'])})
      .catch(res => {this.invalidLogin = true;})
  }

  register(){
    if (this.newPassword !== this.newPassword2)
      return -1;
    let newUserInfo = {username: this.newUsername,
                        email: this.newEmail,
                        password: this.newPassword,
                        first_name: this.newFirstName,
                        last_name: this.newLastName,
			age: this.newAge,
			group: this.newGroup,};
    this.server.post("register/", newUserInfo)
      .then(answer => {console.log(answer)})
      .catch(error => {this.invalidRegister = true;
                        this.errorMessage = error.statusText});
  }

  ngOnInit() {
    if(this.cookie.get('token') != null){
      this.router.navigate(['/dashboard']);
    }
  }

}
