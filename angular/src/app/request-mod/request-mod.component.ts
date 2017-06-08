import { Component, OnInit } from '@angular/core';

import { ServerService } from '../service/server.service';
import { Router } from "@angular/router"

import { CookieService } from 'angular2-cookie/core';

@Component({
  selector: 'app-request-mod',
  templateUrl: './request-mod.component.html',
  styleUrls: ['./request-mod.component.sass']
})
export class RequestModComponent implements OnInit {
  reason: string;
  answer: string;
  errorMessage: string;

  constructor(private server: ServerService) {
  }

  check_request() {
    return true
  }

  send_request(){
    if (!this.check_request())
      return -1;
    let request = {reason: this.reason}
    this.server.post("user/request_mod", request)
      .then(answer => this.answer = answer)
      .catch(error => this.errorMessage = error.statusText);
  }

  ngOnInit() {}
}
