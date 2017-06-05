import { Component, OnInit } from '@angular/core';

import { ServerService } from '../service/server.service';

@Component({
  selector: 'app-profiles',
  templateUrl: './profiles.component.html',
  styleUrls: ['./profiles.component.sass']
})
export class ProfilesComponent implements OnInit {

  profiles: Array<{username: string, id: number, email: string}>;

  profile: number;

  constructor(private server: ServerService) { }

  ngOnInit() {
    this.server.get("list-user/").then(data => this.profiles = data).catch(err => console.log(err))

  }

}
