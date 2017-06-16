import { Component, OnInit } from '@angular/core';

import { CookieService } from 'angular2-cookie/core';

import { Router } from '@angular/router';

import { ServerService } from '../service/server.service';

import { UserService } from '../service/user.service'

@Component({
  selector: 'app-profile-page',
  templateUrl: './profile-page.component.html',
  styleUrls: ['./profile-page.component.sass'],
})
export class ProfilePageComponent implements OnInit {

  constructor(private user: UserService, private cookie: CookieService, private router: Router, private server: ServerService) { }

  ngOnInit() {
  }

}
