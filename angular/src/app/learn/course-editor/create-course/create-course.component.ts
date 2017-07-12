import { Component, OnInit, Input, ComponentRef, ViewChild, ViewContainerRef, ComponentFactoryResolver, ComponentFactory, EventEmitter, Output } from '@angular/core';
import { AddModuleComponent } from '../add-module/add-module.component'
import { Router, ActivatedRoute } from "@angular/router"

import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';

import { CourseService } from '../../../service/course.service'
import { UserService } from "../../../service/user.service"

import { ServerService } from '../../../service/server.service'
@Component({
  selector: 'app-create-course',
  templateUrl: './create-course.component.html',
  styleUrls: ['./create-course.component.scss']
})
export class CreateCourseComponent {

  @ViewChild('modules', {read: ViewContainerRef}) modules: ViewContainerRef;
  childComponent: ComponentFactory<AddModuleComponent>;
  moduleArray: ComponentRef<AddModuleComponent>[] = [];
  length: number = 0;
  error = false;

  loading = true;


  categories: {};
  category: number;

  setCategory(id: number){
    this.category = id;
  }

  title: string;

  setTitle(title: string){
    this.title = title;
  }

  validSave = true;

  public courseForm = new FormGroup({
    title: new FormControl("title", Validators.required),
    category: new FormControl('category', Validators.required),
  })

  @Output() emitter: EventEmitter<any> = new EventEmitter();

  ngAfterViewInit(){
    if(!this.user.isModerator()){
      //this.router.navigate(["/course/page-not-found"])
    }
    this.length = this.modules.length
  }

  constructor(
    public router: Router,
    public route: ActivatedRoute,
    public server: ServerService,
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

  addModule(title?: string, moduleDescription?: string, questions?: Array<any>){
    let moduleComponent = this.modules.createComponent(this.childComponent);
    let module = (<AddModuleComponent> moduleComponent.instance)
    if(title != null){
      module.title = title
    }
    if(moduleDescription != null){
      module.learningText = moduleDescription
    }
    if(questions != null){
      for(let i = 0; i < questions.length; i++){
        let question = questions[i]
        module.editQuestion(question['class'], question['question_body'], question['answers'], question['feedback'])
      }
    }
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
    let saveModules = this.saveModules(f)
    if(f.valid){
      let course = {title: f.value['title'], categorie: f.value['category'],  modules: saveModules};
      console.log(course)
      this.uploadState(course);
    }
  }

  saveModules(form){
    let saveModules = [];
    for(let i = 0; i < this.moduleArray.length; i++){
      let module = this.moduleArray[i];
      let index = this.modules.indexOf(module.hostView);
      let m = (<AddModuleComponent> module.instance).save(form);
      m['order'] = index
      saveModules.push(m)
    }
    return saveModules
  }

  uploadState(course){
    this.server.post('save/course/', course)
    .then(data => {
      this.course.load()
      this.router.navigate(['/course'])
    }).catch(err => {
      console.log(err)
    })
  }


}
