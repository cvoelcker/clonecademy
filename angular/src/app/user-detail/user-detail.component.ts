import {Component, OnInit, Input} from '@angular/core';
import { ServerService } from '../service/server.service';
import { ProfilesComponent } from '../profiles/profiles.component'

@Component({
  selector: 'app-user-detail',
  templateUrl: './user-detail.component.html',
  styleUrls: ['./user-detail.component.sass']
})

export class UserDetailComponent implements OnInit{

  @Input() id: number;

  user: {username: string, id: number, email: string, group: {}, dateRegistered: Date, dateString: string}

  constructor(private server: ServerService) { }

  ngOnInit() {
    this.server.get("user/"+ this.id + "/").then(data => {
      this.user = data
      this.user['dateRegistered'] = new Date(data['date_registered'])
    }).catch(err => console.log(err))


  }
}
