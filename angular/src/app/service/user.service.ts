import { Injectable } from '@angular/core';

import { ServerService } from './server.service'

import { Router } from "@angular/router"

import {CookieService} from 'angular2-cookie/core';


@Injectable()
export class UserService {

  public login: boolean = false;
  public username: string;
  public dateJoined: Date;
  private id: number;
  public email: string;
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
          this.username = data['username']
          this.id = data['id']
          this.email = data['email']
          this.groups = data['groups']
          this.dateJoined = new Date(data['date_joined'])
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
    return this.isInGroup("moderator")
  }

  public logout(){
    this.login = false
    this.cookie.removeAll();
    this.server.clearToken();
    this.router.navigate(['/login']);
  }

  constructor(private server: ServerService, private router: Router, private cookie: CookieService ) {
    this.login = this.server.getToken() != null
    this.loadUser()
  }

}
