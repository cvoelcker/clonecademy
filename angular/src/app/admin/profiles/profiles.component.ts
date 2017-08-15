import { Component, OnInit, ViewChild } from '@angular/core';

import { ServerService } from '../../service/server.service';

import { Router } from "@angular/router"

import { UserDetailComponent } from '../user-detail/user-detail.component'

//import { UserDetailComponent } from '../user-detail/user-detail.component'

@Component({
  selector: 'app-profiles',
  templateUrl: './profiles.component.html',
  styleUrls: ['./profiles.component.sass']
})
export class ProfilesComponent implements OnInit {

  // Array<{username: string, id: number, email: string}>
  profiles: any;

  loading = true;

  selectedValue: number;

  constructor(private server: ServerService, private router: Router) { }

  ngOnInit() {
    // load the data for the current user
    this.server.get("user/", true)
      .then(data => {
        this.profiles = data;
        this.loading = false;
      })
  }

  // change to see the details for another user
  change(id: number){
    this.router.navigate(['/admin/profiles/' + id])
  }


}
