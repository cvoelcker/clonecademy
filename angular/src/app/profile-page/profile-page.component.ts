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

  constructor(private cookie: CookieService, private router: Router, private server: ServerService) { }

  ngOnInit() {
  }

  logout(): void{
    this.cookie.removeAll();
    this.router.navigate(['/login'])
    this.server.clearToken();
  }

}
