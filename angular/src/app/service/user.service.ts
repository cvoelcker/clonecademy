import { Injectable } from '@angular/core';

import { ServerService } from './server.service'

import { Router } from "@angular/router"

import {CookieService} from 'angular2-cookie/core';


@Injectable()
export class UserService {

  public login: boolean;
  public username: string;
  public dateJoined: Date;
  private id: number;
  public email: string;

  public loginUser(username: string, password: string){
    return new Promise((resolve, reject) =>  this.server.login(username, password)
      .then(res => {
        this.loadUser();
        this.login = true;
        this.router.navigate(['/dashboard']);
        resolve(true)
      })
      .catch(res => {
        console.log(res)
        reject(res)
      })
    )
  }

  public loadUser(){
    this.server.get("current_user/").then(data => {
      this.username = data.user['username']
      this.id = data.user['id']
      this.email = data.user['email']

      this.dateJoined = new Date(data['user']['date_joined'])
    }).catch(err => console.log(err))
  }

  public logout(){
    this.login = false
    this.cookie.removeAll();
    this.server.clearToken();
    this.router.navigate(['/login']);
  }

  constructor(private server: ServerService, private router: Router, private cookie: CookieService ) {
    this.login = this.server.getToken() != null
  }

}
