import { Component, OnInit, Input } from '@angular/core';

import { ServerService} from '../service/server.service'

@Component({
  selector: 'personal-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.css']
})
export class StatisticsComponent implements OnInit {
  @Input() data: any;
  statisticsString: string;

  constructor(private server: ServerService) {}

  ngOnInit() {
  }

}
