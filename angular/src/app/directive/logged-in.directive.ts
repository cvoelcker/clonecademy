import { Directive, OnDestroy } from '@angular/core';
import { Location } from "@angular/common";
import { Router } from "@angular/router"

import {CookieService} from 'angular2-cookie/core';

@Directive({
  selector: '[appLoggedIn]'
})
export class LoggedInDirective implements OnDestroy {

  constructor(private cookie: CookieService, private router: Router, private location: Location) {

    if(!this.cookie.get("token") != null){ // if not logged in
      this.location.replaceState("/"); // clear browser history
      this.router.navigate(["/login"]); // go back to login page
    }
  }

  ngOnDestroy() {
        this.cookie.removeAll()
    }

}
