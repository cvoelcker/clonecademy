import { Component, OnInit } from '@angular/core';

import { UserService } from '../../service/user.service'

@Component({
  selector: 'app-admin-page',
  templateUrl: './admin-page.component.html',
  styleUrls: ['./admin-page.component.sass']
})
export class AdminPageComponent implements OnInit{

  // the pages for the admin
  menu: Array<{name: string, url: string}> = [
    {name: "Profiles", url: "profiles"}
  ]


  ngOnInit() {
  }

}
