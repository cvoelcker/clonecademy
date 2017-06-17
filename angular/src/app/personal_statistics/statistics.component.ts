import { Component, OnInit, Input } from '@angular/core';

import { ServerService} from '../service/server.service';

@Component({
  selector: 'statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.scss']
})
export class StatisticsComponent implements OnInit {
  statistics: JSON;
  loading = true

  constructor(private server: ServerService) {
  }

  ngOnInit() {
    this.server.get("user/statistics", true)
      .then(data => {
        this.statistics = data
        this.loading = false
        }
      )
  }

}
