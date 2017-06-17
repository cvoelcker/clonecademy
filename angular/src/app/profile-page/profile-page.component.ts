import { Component, Type, OnInit, Output, EventEmitter, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory } from '@angular/core';

import { CookieService } from 'angular2-cookie/core';

import { ActivatedRoute, Params, Router } from '@angular/router'

import { ServerService } from '../service/server.service';

import { UserService } from '../service/user.service'

// import all modules for all buttons.
import { RequestModComponent } from '../request-mod/request-mod.component';
import { StatisticsComponent } from "../personal_statistics/statistics.component";
import { UserDetailComponent } from '../user-detail/user-detail.component'

@Component({
  selector: 'app-profile-page',
  templateUrl: './profile-page.component.html',
  styleUrls: ['./profile-page.component.sass'],
})
export class ProfilePageComponent implements OnInit {

  menu = [
    {name: "User details", comp: UserDetailComponent, url: "user_details"},
    {name: "Reqeust Mod rights", comp: RequestModComponent, url: "request_mod" },
    {name: "Statistics", comp: StatisticsComponent, url: "statistics"}
  ]

  item: any;

  @ViewChild('content', {read: ViewContainerRef}) content: ViewContainerRef;

  constructor(
    private route: ActivatedRoute,
    private factory: ComponentFactoryResolver,
    private user: UserService,
    private cookie: CookieService,
    private router: Router,
    private server: ServerService
  ) {

  }

  ngOnInit() {
    this.route.params.subscribe(data => {
      if(data.subpage != null){
        for(let i = 0; i < this.menu.length; i++){
          if(this.menu[i].url === data.subpage){
            this.load(this.menu[i])
          }
        }
      }
    })
  }

  load(m){
    this.router.navigate(["profile/" + m.url])
    let item = this.factory.resolveComponentFactory(m.comp)
    this.content.clear()
    this.content.createComponent(item)
  }

}
