import { Component, OnInit, ViewChild } from '@angular/core';

import { ServerService } from '../service/server.service';

import { Router } from "@angular/router"

import { UserDetailComponent } from '../user-detail/user-detail.component'

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

  @ViewChild('user', {read: UserDetailComponent}) user: UserDetailComponent;


  constructor(private server: ServerService, private router: Router) { }

  ngOnInit() {
    this.server.get("list-user/").then(data => this.profiles = data).catch(err => console.log(err))
  }

  changed(){
    if(this.user != undefined){
      this.user.ngOnInit()
    }
  }


}
