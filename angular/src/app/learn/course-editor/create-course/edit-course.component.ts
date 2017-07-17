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
      console.log(data)
      super.setCategory(data['category'][0])
      super.setTitle(data['name'])
      for(let i = 0; i < data['module'].length; i++){
        let module = data['module'][i]
        super.addModule(module['name'], module['learning_text'], module['questions'])
      }
    })
  }

}
