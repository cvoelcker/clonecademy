import { Component, OnInit } from '@angular/core';

import { ServerService} from '../service/server.service'


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  course: any;

  constructor(private server: ServerService) {

  }

  connect(){
    this.server.get("courses").then(data => this.course = data).catch(err => console.log(err))
  }

  ngOnInit() {
  }

}
