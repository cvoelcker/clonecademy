import { Component, OnInit, Input } from '@angular/core';

import { Http, RequestOptions, Headers } from '@angular/http';

import {CookieService} from 'angular2-cookie/core';
import { ServerService } from '../../service/server.service'

import 'rxjs/Rx' ;

@Component({
  selector: 'statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.scss']
})
export class StatisticsComponent implements OnInit {
  statistics: {};
  loading = true

  constructor(private server: ServerService, private cookie: CookieService, private http: Http) {
  }

  ngOnInit() {
    this.server.get("user/statistics", true, false)
      .then(data => {
        this.statistics = data;
        for(let s in this.statistics){
          s["date"] = new Date(s["date"]);
        }
        this.loading = false;
      })
        .catch(err => {
        this.loading = false;
      })
  }

  downloadStatistics(){
    this.server.post("user/statistics/download", {})
    .then(data => {
      // create the file to download
      let blob = new Blob([data["_body"]], {type: "text/csv"});
      let downloadData = URL.createObjectURL(blob)
      // create a button which will be clicked to download
      // at the moment it looks like this is the only workaround for a download dialog
      var anchor = document.createElement("a");
      // set download name
      anchor.download = "statistics.csv";
      anchor.href = downloadData;
      // hide button
      anchor.setAttribute('visibility', "hidden")
      anchor.setAttribute("display", "none")
      // add button to body, activate the download and remove the button again
      document.body.appendChild(anchor)
      anchor.click();
      document.body.removeChild(anchor)
    })
  }

}
