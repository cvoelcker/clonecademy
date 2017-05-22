import { Directive, OnInit } from '@angular/core';


import { ActivatedRoute, Params } from '@angular/router'
import { ServerService } from '../service/server.service';

@Directive({
  selector: '[appModule]'
})
export class ModuleDirective implements OnInit {

  module: any;
  courseID: number;
  moduleID: number;

  constructor(private server: ServerService, private route: ActivatedRoute) { }

  ngOnInit(){
    this.route.params.subscribe((data: Params) => {this.courseID = data.id, this.moduleID = data.module})
    this.server.get("courses/"+this.courseID+"/"+this.moduleID).then(data => {this.module = data; console.log(data)})
  }

}
