import { Component, OnInit, Input, ComponentRef, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory, EventEmitter, Output } from '@angular/core';
import { AddModuleComponent } from '../add-module/add-module.component'
import { Router } from "@angular/router"

import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';

import { CourseService } from '../../../service/course.service'
import { UserService } from "../../../service/user.service"

import { ServerService } from '../../../service/server.service'
@Component({
  selector: 'app-create-course',
  templateUrl: './create-course.component.html',
  styleUrls: ['./create-course.component.scss']
})
export class CreateCourseComponent implements OnInit {

  @ViewChild('modules', {read: ViewContainerRef}) modules: ViewContainerRef;
  childComponent: ComponentFactory<AddModuleComponent>;
  moduleArray: ComponentRef<AddModuleComponent>[] = [];
  length: number = 0;
  error = false;

  loading = true;


  categories: {};
  catId: number;

  validSave = true;

  public courseForm = new FormGroup({
    title: new FormControl("title", Validators.required),
    category: new FormControl('category', Validators.required),
  })

  @Output() emitter: EventEmitter<any> = new EventEmitter();

  ngOnInit(){
    if(!this.user.isModerator())
    this.router.navigate(["/course/page-not-found"])
    this.length = this.modules.length
  }

  constructor(
    private router: Router,
    private server: ServerService,
    private componentFactory: ComponentFactoryResolver,
    private course: CourseService,
    private user: UserService,
    private fb: FormBuilder,
  ) {
    this.childComponent = this.componentFactory.resolveComponentFactory(AddModuleComponent)
    this.server.get("get-course-categories/", true)
      .then(data => {
        this.categories = data;
        this.loading = false;
      })
  }

  addModule(){
    let moduleComponent = this.modules.createComponent(this.childComponent);
    let module = (<AddModuleComponent> moduleComponent.instance)
    this.moduleArray.push(moduleComponent)

    module.clear.subscribe((data) => {
      let moduleSingle = moduleComponent
      if(data == "remove"){
        this.moduleArray.splice(this.moduleArray.indexOf(moduleSingle), 1)
        moduleSingle.destroy();
        this.length = this.modules.length;
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
    this.length = this.modules.length;
  }

  removeCourse(){
    this.modules.detach(0)
  }

  save(f){
    let saveModules = [];
    for(let i = 0; i < this.moduleArray.length; i++){
      let module = this.moduleArray[i];
      let index = this.modules.indexOf(module.hostView);
      let m = (<AddModuleComponent> module.instance).save(f);
      m['order'] = index
      saveModules.push(m)
    }
    if(f.valid){
      let course = {title: f.value['title'], categorie: f.value['category'],  modules: saveModules};
      console.log(course)
      // this.server.post('save/course/', course)
      // .then(data => {
      //   this.course.load()
      //   this.router.navigate(['/course'])
      // }).catch(err => {
      //   console.log(err)
      // })
    }
  }


}
