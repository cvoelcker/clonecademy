import {Component, OnInit, Input} from '@angular/core';
import { ServerService } from '../service/server.service';
import { ProfilesComponent } from '../profiles/profiles.component'

@Component({
  selector: 'app-user-detail',
  templateUrl: './user-detail.component.html',
  styleUrls: ['./user-detail.component.sass']
})

export class UserDetailComponent {

  user: {username: string, id: number, email: string, group: {}, dateRegistered: Date, dateString: string}

  constructor(private server: ServerService) { }

  change(id: number){
    this.server.get("user/"+ id + "/").then(data => {
      this.user = data
      this.user['dateRegistered'] = new Date(data['date_joined'])
    }).catch(err => console.log(err))
  }
}
