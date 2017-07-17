import {Component, OnInit, Input} from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router'
import { ServerService } from '../../service/server.service';
import { ProfilesComponent } from '../profiles/profiles.component'

@Component({
  selector: 'app-user-detail',
  templateUrl: './user-detail.component.html',
  styleUrls: ['./user-detail.component.sass']
})

export class UserDetailComponent {

  // {username: string, id: number, email: string, group: {}, dateRegistered: Date, dateString: string}
  user: any;
  id: number;

  constructor(
    private route: ActivatedRoute,
    private server: ServerService,
    private router: Router,
  ) {
    this.route.params.subscribe(data => {
      this.id = data.id
      this.change(this.id);
    })
  }

  change(id: number){
    this.server.get("user/"+ id + "/")
    .then(data => {
      this.user = data
      this.user['dateRegistered'] = new Date(data['date_joined'])
    })
    .catch(err => console.log(err))
  }
}
