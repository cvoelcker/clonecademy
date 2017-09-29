import {Directive, ViewContainerRef} from '@angular/core';

import {ActivatedRoute, Params} from '@angular/router'

@Directive({
  selector: '[appModule]'
})
export class ModuleDirective {
  constructor(public viewContainerRef: ViewContainerRef) {
  }
}
