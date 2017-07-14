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

  usernameToPromote: string;

  constructor(private server: ServerService) { }

  change(id: number){
    this.server.get("user/"+ id + "/").then(data => {
      console.log(data)
      this.user = data
      this.user["username"] = data["user"].username
      this.user["email"] = data["user"].email
      this.user.id = id
      /* this.user['dateRegistered'] = new Date(data['date_joined']) */
      console.log(this.user)
    }).catch(err => console.log(err))
  }

  grantCurrentUserModStatus(){
    console.log(this.user["id"]);
    this.server.post("user/"+ this.user["id"] + "/grantModStatus/", {})
      .then(answer => {console.log(answer)})
  }

  grantEnteredUserModStatus(){
    let usernameJSON = {username: this.usernameToPromote,};
    this.server.post("user/grant_mod/", usernameJSON)
      .then(answer => {console.log(answer)})
  }

}
