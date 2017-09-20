import {Component, OnInit} from '@angular/core';
import {trigger, state, style, animate, transition} from '@angular/animations';
import {Router} from '@angular/router';
import {CookieService} from 'angular2-cookie/core';

import {ErrorDialog} from '../service/error.service'
import {UserService} from '../service/user.service';
import {ServerService} from '../service/server.service'



@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  animations: [
    trigger('show', [
      state('active', style({
        display: 'none'
      })),
      state('inactive', style({
        display: 'block'
      })),
      transition('inactive => active', animate('100ms ease-in')),
    ])
  ]
})
export class LoginComponent implements OnInit {

  username: string;
  password: string;
  submitted: boolean;
  invalidLogin: boolean;

  constructor(private errorDialog: ErrorDialog, private cookie: CookieService,
    public server: ServerService, public user: UserService,
    private router: Router) {

  }

  login(form) {
    if (form.valid) {
      this.user.loginUser(this.username, this.password)
        .catch(data => {
          this.errorDialog.open(data['non_field_errors'][0])
        })
    } else {
      this.errorDialog.open('Username and password is required')
    }
  }

  ngOnInit() {
    if (this.cookie.get('token') != null) {
      this.router.navigate(['/course']);
    }
  }
}
