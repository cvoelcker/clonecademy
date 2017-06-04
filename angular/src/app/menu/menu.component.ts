import { Component, OnInit } from '@angular/core';

import { CookieService } from 'angular2-cookie/core';

import { Router } from '@angular/router';

import { ServerService } from '../service/server.service';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})
export class MenuComponent implements OnInit {

  logout(): void{
    this.cookie.removeAll();
    this.router.navigate(['/login'])
    this.server.clearToken();
  }

  constructor(private cookie: CookieService, private router: Router, private server: ServerService) {

  }

  ngOnInit() {
  }

}
