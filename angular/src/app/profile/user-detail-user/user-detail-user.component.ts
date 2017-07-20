import {Component, OnInit, Input} from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router'
import { UserService } from '../../service/user.service';
import { ServerService } from '../../service/server.service';
import { ProfilePageComponent } from '../profile-page/profile-page.component';
import { ErrorDialog } from "../../service/error.service"
import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-user-detail-user',
  templateUrl: './user-detail-user.component.html',
  styleUrls: ['./user-detail-user.component.sass']
})

export class UserDetailUserComponent {
  // {username: string, id: number, email: string, group: {}, dateRegistered: Date, dateString: string}

  constructor(
    private user: UserService,
    private server: ServerService,
    ) {}

    ngOnInit() {
      }

      edit(value){
          let data = value.value
          this.server.post("user/current", data, false, false)
        }

  }
