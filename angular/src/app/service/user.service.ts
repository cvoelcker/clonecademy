import { Injectable } from '@angular/core';

import { ServerService } from './server.service'

import { Router } from "@angular/router"

import {CookieService} from 'angular2-cookie/core';

import {TranslateService} from '@ngx-translate/core';


@Injectable()
export class UserService {

  public login: boolean = false;
  public data: any;
  private groups: Array<string>;
  public id: number;
  public language: string = "en";

  public loaded = false;

  public loginUser(username: string, password: string){
    return new Promise((resolve, reject) =>  this.server.login(username, password)
      .then(res => {
        this.loadUser().then(() => {
          this.router.navigate(['/course']);
          this.login = true;
          resolve(true)
        });


      })
      .catch(res => {
        console.log(res)
        reject(res)
      })
    )
  }

  public loadUser(){

    return new Promise((resolve, reject) => this.server.get("user/current", true, false).then(data => {
          this.groups = data['groups'];
          this.data = data;
          this.loaded = true;
          this.id = data['id']
          this.language = data['language']
          this.translate.use(data['language']);
          resolve()
        })
        .catch(err => {
          this.loaded = true;
          reject()
        })
      )
  }

  private isInGroup(name: string){
    if(this.loaded && this.login){
      for(let i = 0; i < this.groups.length; i++){
        if(this.groups[i] == name){
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

  public edit(data){
    this.server.post("user/current", data).then(() => {
      this.translate.use(data['language'])
    })
  }

  constructor(private translate: TranslateService, private server: ServerService, private router: Router, private cookie: CookieService ) {
    this.login = this.server.getToken() != null
    if(this.login){
      this.loadUser()
    }
    else{
      this.loaded = true;
    }
  }

}
