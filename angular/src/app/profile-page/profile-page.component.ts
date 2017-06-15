import { Component, OnInit } from '@angular/core';

import { CookieService } from 'angular2-cookie/core';

import { Router } from '@angular/router';

import { ServerService } from '../service/server.service';

@Component({
  selector: 'app-profile-page',
  templateUrl: './profile-page.component.html',
  styleUrls: ['./profile-page.component.sass'],
})
export class ProfilePageComponent implements OnInit {

  user: {username: string, email: string, id: number, date_joined: Date};

  constructor(private cookie: CookieService, private router: Router, private server: ServerService) { }

  ngOnInit() {
    console.log
    this.server.get("current_user/").then(data => {
      this.user = data.user

      this.user['date_joined'] = new Date(data['user']['date_joined'])
    }).catch(err => console.log(err))
  }

  logout(): void{
    this.cookie.removeAll();
    this.router.navigate(['/login'])
    this.server.clearToken();
  }

}
