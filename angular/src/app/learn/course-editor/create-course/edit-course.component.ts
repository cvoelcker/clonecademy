import { Component } from '@angular/core';

import { CreateCourseComponent } from './create-course.component';

@Component({
  selector: 'app-edit-course',
  templateUrl: './create-course.component.html',
  styleUrls: ['./create-course.component.scss']
})
export class EditCourseComponent extends CreateCourseComponent {

  id: number

  ngOnInit() {
    this.route.params.subscribe(data => {
      this.id = data.id
      this.load();
    })
  }

  load(){
    this.server.get('courses/'+(Number(this.id))+'/edit', true, false).then(data => {
      super.setCategory(data['category'])
      super.setTitle(data['name'])
      super.setLanguage(data['language'])
      super.setDifficulty(data['difficulty'])
      for(let i = 0; i < data['modules'].length; i++){
        let module = data['modules'][i]
        super.addModule(module['id'], module['name'], module['learning_text'], module['questions'])
      }
    })
  }

  save(f){
    let saveModules = this.saveModules(f)
    if(f.valid){
      let course = {id: Number(this.id), name: f.value['title'], difficulty: f.value['difficulty'], language: f.value["language"], category: f.value['category'],  modules: saveModules};

      console.log(course)
      //this.uploadState(course);
    }
  }

}
