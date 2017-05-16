import { Directive } from '@angular/core';
import { Router } from "@angular/router"

import { UserService } from '../service/user.service'

@Directive({
  selector: '[appLoggedIn]'
})
export class LoggedInDirective {

  constructor(private user: UserService, private router: Router) {

    if(!this.user.loggedIn()){
      console.log("not logged in")
      this.router.navigate(["/login"])
    }
  }

}
