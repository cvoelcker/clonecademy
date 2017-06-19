import { Injectable } from '@angular/core';

import { ServerService } from './server.service'

import { Router } from "@angular/router"

import {CookieService} from 'angular2-cookie/core';


@Injectable()
export class UserService {

  public login: boolean = false;
  private groups: Array<{name: string}>;

  public loaded = false;

  public loginUser(username: string, password: string){
    return new Promise((resolve, reject) =>  this.server.login(username, password)
      .then(res => {
        this.login = true;
        this.loadUser().then(() => {this.router.navigate(['/course']); resolve(true)});

      })
      .catch(res => {
        console.log(res)
        reject(res)
      })
    )
  }

  public loadUser(){

    return new Promise((resolve, reject) => this.server.get("current_user/", true, false).then(data => {
          this.groups = data['groups']
          this.loaded = true;
          resolve()
        })
        .catch(err => {
          this.loaded = true;
          reject()
        })
      )
  }

  private isInGroup(name: string){
    if(this.loaded){

      for(let i = 0; i < this.groups.length; i++){
        if(this.groups[i].name == name){
          return true;
        }
      }
    }
    return false;
  }

  public isAdmin(){
    return this.isInGroup('admin')
  }

  public isModerator(){
    return this.isInGroup('admin') || this.isInGroup("moderator")
  }

  public logout(){
    this.login = false
    this.groups = null;
    this.cookie.removeAll();
    this.server.clearToken();
    this.router.navigate(['/login']);
  }

  constructor(private server: ServerService, private router: Router, private cookie: CookieService ) {
    this.login = this.server.getToken() != null
    this.loadUser()
  }

}
