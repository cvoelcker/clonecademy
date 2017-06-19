import { Injectable } from '@angular/core';

import { ServerService } from './server.service'

@Injectable()
export class CourseService {

  data: any

  constructor(private server: ServerService) {
  }

  load(){
    return new Promise((resolve, reject) => this.server.get("courses/", true)
      .then(data => {
        this.data = data
        resolve()
        }
      )
      .catch(err => {
        reject()
      })
    )
  }

}
