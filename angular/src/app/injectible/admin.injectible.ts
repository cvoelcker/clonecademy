import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { UserService } from '../service/user.service';


@Injectable()
export class Admin implements CanActivate {

  constructor(private router: Router, private user: UserService) {}

  canActivate() {
    if(!this.user.isAdmin()){
      this.router.navigate(["/404"])
    }
    return this.user.isAdmin()
  }
}
