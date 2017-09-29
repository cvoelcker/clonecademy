import {Component, Input} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router'
import {ServerService} from '../../service/server.service';
import {UserService} from '../../service/user.service';
import {ProfilesComponent} from '../profiles/profiles.component'

/**
Make the user details visible to the admin and add some more admin funktions for users
@author Ilhan Simsiki
**/
@Component({
  selector: 'app-user-detail',
  templateUrl: './user-detail.component.html',
  styleUrls: ['./user-detail.component.sass']
})

export class UserDetailComponent {

  user: any;
  id: number;
  isMod = false;
  isAdmin = false;

  loading = true;

  constructor(
    private route: ActivatedRoute,
    private server: ServerService,
    private router: Router
  ) {
    this.route.params.subscribe(data => {
      this.id = data.id
      this.change(this.id);
    })
  }

  /**
    This funktions loads the user with the id, gives the variable "user" the
    response and sets the variables isMod, isAdmin

    @param id: the id number of the user to load from the server
    @author Ilhan Simisiki
  **/
  change(id: number) {
    this.loading = true;
    // load the current user
    this.server.get('user/' + id + '/')
      .then(data => {
        this.user = data
        this.user['dateRegistered'] = new Date(data['date_joined'])
        this.isMod = (-1 !== this.user['groups'].indexOf('moderator'));
        this.isAdmin = (-1 !== this.user['groups'].indexOf('admin'));

        // show the spinning loader until the user is loaded
        this.loading = false;
      })
  }

  /**
  Promote or demote a user to admin or moderator and reset the current user information

  @param
    right: a string for the group ('admin' or 'moderator')
    action: a string for 'demote' or 'promote'
  @author Tobias Huber
  **/
  proDemote(right: string, action: string) {
    this.server.post('user/' + this.id + '/rights', {
      'right': right,
      'action': action
    })
    .then(data => {
      this.isMod = (-1 !== data['groups'].indexOf('moderator'))
      this.isAdmin = (-1 !== data['groups'].indexOf('admin'))
    })
  }
}
