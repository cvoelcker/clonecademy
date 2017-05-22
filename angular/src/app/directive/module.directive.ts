import { Directive, ViewContainerRef } from '@angular/core';


import { ActivatedRoute, Params } from '@angular/router'
import { ServerService } from '../service/server.service';

@Directive({
  selector: '[appModule]'
})
export class ModuleDirective{


  constructor(public viewContainerRef: ViewContainerRef) { }



}
