import { Component, OnInit } from '@angular/core';

import {CookieService} from 'angular2-cookie/core';

import { UserService } from '../service/user.service'

import { Http} from '@angular/http';

import {MdDialog, MdDialogRef} from '@angular/material';

import {MdButtonModule} from '@angular/material';

import {MdMenuModule} from '@angular/material';

import { DialogComponent } from "../quickview/dialog.component";

 // import { DialogContentExample } from '../dialog-content/dialog-content-example.component';



@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})

export class MenuComponent implements OnInit {

  links: Array<{url: string, name: string}> = [
    {url: "about", name: "About"},
    {url: 'impressum', name: "Impressum"},
  ]
  login: boolean;

  constructor(private cookie: CookieService, private user: UserService, public http: Http, public dialog: MdDialog){
    this.login = this.cookie.get("token") != null
  }

  ngOnInit() {
  }

  openDialog(key) {
  let dialogRef = this.dialog.open(DialogComponent);
}

}
