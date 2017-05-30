import { Component, OnInit, Input, ComponentRef, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory, EventEmitter } from '@angular/core';
import { AddModuleComponent } from '../add-module/add-module.component'
@Component({
  selector: 'app-create-course',
  templateUrl: './create-course.component.html',
  styleUrls: ['./create-course.component.css']
})
export class CreateCourseComponent implements OnInit {

  @Input() title: string;
  @ViewChild('modules', {read: ViewContainerRef}) modules: ViewContainerRef;
  childComponent: ComponentFactory<AddModuleComponent>;
  moduleArray: ComponentRef<AddModuleComponent>[] = [];
  i = 0;

  constructor(private componentFactory: ComponentFactoryResolver) {
    this.childComponent = this.componentFactory.resolveComponentFactory(AddModuleComponent)
  }

  ngOnInit() {
  }

  addModule(){
    let moduleComponent = this.modules.createComponent(this.childComponent);
    let module = (<AddModuleComponent> moduleComponent.instance)
    this.moduleArray.push(moduleComponent)

    module.clear.subscribe((data) => {
      if(data == "remove"){
        moduleComponent.destroy();
      }
      else if(data == "up"){
        let index = this.modules.indexOf(moduleComponent.hostView);
        let i = index - 1 > 0 ? index - 1 : 0;
        this.modules.move(moduleComponent.hostView, i);
      }
      else if(data == "down"){
        let index = this.modules.indexOf(moduleComponent.hostView);
        let i = index + 1 < this.moduleArray.length ? index + 1 : this.moduleArray.length - 1;
        this.modules.move(moduleComponent.hostView, i);
      }
    })
  }

  removeCourse(){

    this.modules.detach(0)
  }

  save(){

    this.modules.length
    for(let i = 0; i < this.moduleArray.length; i++){
      let module = this.moduleArray[i];
      let index = this.modules.indexOf(module.hostView);
      let m = (<AddModuleComponent> module.instance).save();
      if(index >= 0 && m != null){
        //console.log(m)
      }
    }

  }

}
