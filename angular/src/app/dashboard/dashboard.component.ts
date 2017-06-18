import { Component, OnInit,} from '@angular/core';

import { ServerService} from '../service/server.service'

import { trigger, state, style, animate, transition } from '@angular/animations';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  animations: [
    trigger('show', [
      state( "active", style({
        display: "none"
      })),
      state( "inactive", style({
        display: "block"
      })),
      transition('inactive => active', animate('100ms ease-in')),
    ])
  ]
})
export class DashboardComponent implements OnInit {
  data: any;
  collapse: boolean

  loading = true;


  constructor(private server: ServerService) {

  }

  ngOnInit() {

    // load the list of courses from the server
    this.server.get("courses/", true)
      .then(data => {
        this.data = data
        this.loading = false;
        }
      )

  }

}
