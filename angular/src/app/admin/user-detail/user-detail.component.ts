import {Component, OnInit, Input} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router'
import {ServerService} from '../../service/server.service';
import {UserService} from '../../service/user.service';
import {ProfilesComponent} from '../profiles/profiles.component'

@Component({
  selector: 'app-user-detail',
  templateUrl: './user-detail.component.html',
  styleUrls: ['./user-detail.component.sass']
})

export class UserDetailComponent {

  // {username: string, id: number, email: string, group: {}, dateRegistered: Date, dateString: string}
  user: any;
  id: number;
  isMod = false;
  isAdmin = false;

  loading = true;

  position = 'before';

  constructor(private route: ActivatedRoute,
              private server: ServerService,
              private router: Router,) {
    this.route.params.subscribe(data => {
      this.id = data.id
      this.change(this.id);
    })
  }

  ngOnInit() {

  }

  change(id: number) {
    this.loading = true;
    // load the current user
    this.server.get("user/" + id + "/")
      .then(data => {
        this.user = data
        this.user['dateRegistered'] = new Date(data['date_joined'])
        this.isMod = (-1 != this.user["groups"].indexOf("moderator"));
        this.isAdmin = (-1 != this.user["groups"].indexOf("admin"));

        // show the spinning loader until the user is loaded
        this.loading = false;
      })
      .catch(err => console.log(err))
  }

  promoteToModerator() {
    this.server.post("user/" + this.id + "/rights", {
      "right": "moderator",
      "action": "promote"
    })
      .then(answer => {
        this.isMod = true;
      })
  }

  promoteToAdmin() {
    this.server.post("user/" + this.id + "/rights", {
      "right": "admin",
      "action": "promote"
    })
      .then(answer => {
        this.isAdmin = true;
      })
  }

  demoteToUser() {
    this.server.post("user/" + this.id + "/rights", {
      "right": "moderator",
      "action": "demote"
    })
      .then(answer => {
        this.isMod = false;
        console.log(answer)
      })
      .catch(err => console.log(err))
  }

  demoteToModerator() {
    this.server.post("user/" + this.id + "/rights", {
      "right": "admin",
      "action": "demote"
    })
      .then(answer => {
        this.isAdmin = false;
        console.log(answer)
      })
      .catch(err => console.log(err))
  }
}
