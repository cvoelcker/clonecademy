import {Component, OnInit, Input} from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router'
import { UserService } from '../../service/user.service';
import { ProfilePageComponent } from '../profile-page/profile-page.component';

@Component({
  selector: 'app-user-detail-user',
  templateUrl: './user-detail-user.component.html',
  styleUrls: ['./user-detail-user.component.sass']
})

export class UserDetailUserComponent {
  // {username: string, id: number, email: string, group: {}, dateRegistered: Date, dateString: string}

  constructor(
    private user: UserService,
    ) {}

    ngOnInit() {
      
      }
  }
