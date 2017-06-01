import { Component, OnInit, Input, ComponentRef, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory, EventEmitter } from '@angular/core';
import { AddModuleComponent } from '../add-module/add-module.component'

import { ServerService } from '../service/server.service'
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

  categories: {name: string, id: number};
  catId: number;

  constructor(private server: ServerService, private componentFactory: ComponentFactoryResolver) {
    this.childComponent = this.componentFactory.resolveComponentFactory(AddModuleComponent)
  }

  ngOnInit() {
    this.server.get("get-course-categories/").then(data => this.categories = data).catch(err => console.log(err))
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

    let saveModules = [];
    for(let i = 0; i < this.moduleArray.length; i++){
      let module = this.moduleArray[i];
      let index = this.modules.indexOf(module.hostView);
      let m = (<AddModuleComponent> module.instance).save();
      if(index >= 0 && m != null){
        m['order'] = index
        saveModules.push(m)
      }
    }
    let course = {title: this.title, categorie: this.catId,  modules: saveModules};
    this.server.post('save/course/', course).then(data => {console.log(data)}).catch(err => {console.log(err)})

  }

}
