import { Component, OnInit } from '@angular/core';

import { ServerService } from '../../service/server.service';
import { Router } from "@angular/router"

import { CookieService } from 'angular2-cookie/core';

@Component({
  selector: 'app-request-mod',
  templateUrl: './request-mod.component.html',
  styleUrls: ['./request-mod.component.sass']
})
export class RequestModComponent implements OnInit {
  reason: string;
  errorMessage: string;
  available: boolean;
  loading = true;


  constructor(private server: ServerService) {}

  check_request() {
    this.server.get("user/mod_request", true, false)
      .then(answer => {
        this.available = answer['allowed'];
        this.loading = false;
      })
      .catch(error => {
        this.available = false
        this.loading = false;
      });

  }

  send_request(){
    if (!this.available)
      return -1;
    let request = {reason: this.reason}
    this.server.post("user/request_mod", request)
      .then(answer => {this.available=false})
  }

  ngOnInit() {
    this.check_request();
  }

}
