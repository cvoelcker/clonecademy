import { Component } from '@angular/core';

import { CreateCourseComponent } from './create-course.component';

@Component({
  selector: 'app-edit-course',
  templateUrl: './create-course.component.html',
  styleUrls: ['./create-course.component.scss']
})
export class EditCourseComponent extends CreateCourseComponent {

  id: number

  /**
    this reloades the component every time the user clickes on the edit button
  **/
  ngOnChanges(){
    this.load(this.id)
  }

  /**
    on intializing load the component
  **/
  ngOnInit() {
    this.route.params.subscribe(data => {
      this.id = data.id
      this.load(data.id);
    })
  }

  /**
    This Function loads the current course from the id variable.
    If the course does not exist in the database nothing will happen.
  **/
  load(id: number){
    // this variable has to be set for the progress loader
    super.setCourseTrue(false)
    this.server.get('courses/'+(Number(id))+'/edit', true, false).then(data => {
      super.setDescription(data['description'])
      super.setCategory(data['category'])
      super.setTitle(data['name'])
      super.setLanguage(data['language'])
      super.setDifficulty(data['difficulty'])
      super.clearModule()
      this.quiz = data['quiz']
      for(let i = 0; i < data['modules'].length; i++){
        let module = data['modules'][i]
        super.addModule(module['id'], module['name'], module['learning_text'], module['questions'])
      }
      super.setCourseTrue(true)
    })
  }

  /**
    save the current course with the old id and the old modules
  **/
  save(f){
    let saveModules = this.saveModules(f)
    if(f.valid){
      for(let q of this.quiz ){
        delete q.invisible;
      }
      let course = {
        id: Number(this.id),
        name: f.value['title'],
        difficulty: f.value['difficulty'],
        language: f.value["language"],
        category: f.value['category'],
        modules: saveModules,
        quiz: this.quiz,
        description: this.description
      };
      this.uploadState(course);
    }
  }

}
