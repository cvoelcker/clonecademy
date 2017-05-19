import { Component, OnInit } from '@angular/core';

import { ServerService} from '../service/server.service'


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  constructor(private server: ServerService) {

  }

  connect(){
    this.server.get("courses").catch(err => console.log(err))
  }

  ngOnInit() {
  }

}
