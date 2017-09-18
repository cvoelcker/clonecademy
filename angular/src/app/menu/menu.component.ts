import {Component, OnInit} from '@angular/core';
import {CookieService} from 'angular2-cookie/core';
import {Http} from '@angular/http';
import {MdDialog, MdDialogRef, MdButtonModule, MdMenuModule, MdSidenavModule} from '@angular/material';
import {UserService} from '../service/user.service'
import {DialogComponent} from '../quickview/dialog.component';


@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})

export class MenuComponent implements OnInit {

  links: Array<{ url: string, name: string }> = [
    {url: 'about', name: 'About'},
    {url: 'impressum', name: 'Impressum'},
  ]
  login: boolean;

  constructor(private cookie: CookieService, private user: UserService, public http: Http,
              public dialog: MdDialog) {
    this.login = this.cookie.get('token') != null
  }

  ngOnInit() {
  }

  openDialog(key) {
    const dialogRef = this.dialog.open(DialogComponent, {
      height: '250px',
      width: '250px',
    });
    dialogRef.updatePosition({top: '65px', right: '3px'});
  }

}
