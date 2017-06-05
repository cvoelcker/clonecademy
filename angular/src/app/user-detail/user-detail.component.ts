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

  user: Array<{username: string, id: number, email: string}>;

  constructor(private server: ServerService) { }

  ngOnInit() {
    this.server.get("list-user/").then(data => this.user = data).catch(err => console.log(err))
    

  }
}
