import { Injectable } from '@angular/core';

import { ServerService, User } from './server.service';

import { CookieService } from 'angular2-cookie/core';

import { Router } from "@angular/router"



@Injectable()
export class UserService {

  id: number;
  name: string;
  token: string;

  valid: boolean;

  constructor(private server: ServerService, private cookie: CookieService, private router: Router) {
    this.name = this.cookie.get('userName')
  }

  loggedIn(): boolean {
    return this.name != null
  }

  login(name: string, password: string){
    return this.server.login(name, password).then(
      valid => {
        this.name = name;
        this.cookie.put("userName", name);
      })
  }

  logout(): void{
    this.id = null;
    this.name = null;
    this.cookie.removeAll();
    this.router.navigate(['/login'])
  }

}
