import { Directive, OnDestroy } from '@angular/core';
import { Location } from "@angular/common";
import { Router } from "@angular/router"

import { UserService } from '../service/user.service'

@Directive({
  selector: '[appLoggedIn]'
})
export class LoggedInDirective implements OnDestroy {

  constructor(private user: UserService, private router: Router, private location: Location) {

    if(!this.user.loggedIn()){ // if not logged in
      this.location.replaceState("/"); // clear browser history
      this.router.navigate(["/login"]); // go back to login page
    }
  }

  ngOnDestroy() {
        if (this.user != null) {
            this.user.logout();
        }
    }

}
