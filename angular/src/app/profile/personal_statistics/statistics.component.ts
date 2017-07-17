import { Component, OnInit, Input } from '@angular/core';

import { ServerService} from '../../service/server.service';

@Component({
  selector: 'statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.scss']
})
export class StatisticsComponent implements OnInit {
  statistics: {};
  loading = true

  constructor(private server: ServerService) {
  }

  ngOnInit() {
    this.server.get("user/statistics", true, false)
      .then(data => {
        console.log(data)
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

}
