import { Component, OnInit} from '@angular/core';

import { UserService } from '../service/user.service'

@Component({
  selector: 'app-profile-page',
  templateUrl: './profile-page.component.html',
  styleUrls: ['./profile-page.component.sass'],
})
export class ProfilePageComponent implements OnInit {

  // create all items for the list menu
  menu: Array<{name: string, url: string}> = [
    {name: "User details", url: "details"},
    {name: "Reqeust Mod rights", url: "request_mod" },
    {name: "Statistics", url: "statistics"}
  ]

  constructor(private user: UserService){}

  ngOnInit(){

  }


}
