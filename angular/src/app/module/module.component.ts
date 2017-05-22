import { Component, OnInit, ComponentFactoryResolver } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router'
import { ServerService } from '../service/server.service';


@Component({
  selector: 'app-module',
  templateUrl: './module.component.html',
  styleUrls: ['./module.component.css']
})
export class ModuleComponent implements OnInit {

  constructor(private factory: ComponentFactoryResolver, private server: ServerService, private route: ActivatedRoute) { }

  ngOnInit() {

  }

}
