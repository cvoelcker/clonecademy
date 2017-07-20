import {Component, OnInit, Input} from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router'
import { ServerService } from '../../service/server.service';
import { UserService } from '../../service/user.service';
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

  loading = true;

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

  ngOnInit() {
      this.loading = false;
  }

  change(id: number){
  }
}
