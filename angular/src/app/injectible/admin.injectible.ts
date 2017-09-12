import {Injectable} from '@angular/core';
import {CanActivate, Router} from '@angular/router';
import {UserService} from '../service/user.service';


@Injectable()
export class Admin implements CanActivate {

  constructor(private router: Router, private user: UserService) {
  }

  canActivate() {
    // has to check if the user is in the admin group.
    // the request takes to long and propably needs a loading screen on init

    // if(!this.user.isAdmin()){
    //   this.router.navigate(["/404"])
    // }
    // return this.user.isAdmin()
    return true;
  }
}
