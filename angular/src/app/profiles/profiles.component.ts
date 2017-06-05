import { Component, OnInit } from '@angular/core';

import { ServerService } from '../service/server.service';

import { Router } from "@angular/router"

//import { UserDetailComponent } from '../user-detail/user-detail.component'

@Component({
  selector: 'app-profiles',
  templateUrl: './profiles.component.html',
  styleUrls: ['./profiles.component.sass']
})
export class ProfilesComponent implements OnInit {

  profiles: Array<{username: string, id: number, email: string}>;

  profile: number;

  selectedValue = null;

  constructor(private server: ServerService, private router: Router) { }

  ngOnInit() {
    this.server.get("list-user/").then(data => this.profiles = data).catch(err => console.log(err))

  }


}
