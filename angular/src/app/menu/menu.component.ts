import {Component, OnInit} from '@angular/core';

import {CookieService} from 'angular2-cookie/core';

import {UserService} from '../service/user.service'

import {Http} from '@angular/http';

import {MdDialog, MdDialogRef} from '@angular/material';

import {MdButtonModule} from '@angular/material';

import {MdMenuModule} from '@angular/material';

import {DialogComponent} from "../quickview/dialog.component";

import {MdSidenavModule} from '@angular/material';

// import { DialogContentExample } from '../dialog-content/dialog-content-example.component';


@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})

export class MenuComponent implements OnInit {

  links: Array<{ url: string, name: string }> = [
    {url: "about", name: "About"},
    {url: 'impressum', name: "Impressum"},
  ]
  login: boolean;

  constructor(private cookie: CookieService, private user: UserService, public http: Http,
              public dialog: MdDialog) {
    this.login = this.cookie.get("token") != null
  }

  ngOnInit() {
  }

  openDialog(key) {
<<<<<<< HEAD
  let dialogRef = this.dialog.open(DialogComponent, {
  height: '250px',
  width: '250px',
});
  console.log(this.user.data);
  dialogRef.updatePosition({ top: '11%', right: '0.2%' });
}
=======
    let dialogRef = this.dialog.open(DialogComponent, {
      height: '250px',
      width: '250px',
    });
    dialogRef.updatePosition({top: '11%', right: '0.2%'});
  }
>>>>>>> 06c60dc06f90997196524c0127fc4442f0ffc60c

}
