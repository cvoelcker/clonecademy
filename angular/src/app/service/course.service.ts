import {Injectable} from '@angular/core';

import {ServerService} from './server.service'
import {UserService} from './user.service';

@Injectable()
export class CourseService {

  data = {};
  categorys: any;
  started_courses = {};

  constructor(private server: ServerService, private user: UserService) {
  }

  /**
   load courses for all categories for the current user language
   after loading sorts course for every category in data variable
   **/
  load() {
    return new Promise((resolve, reject) => {
      this.getCategory().then(() => {
        let requests = 0
        for (let i = 0; i < this.categorys.length; i++) {
          this.server.post("courses/", {
            "type": "",
            "category": this.categorys[i].name,
            "language": this.user.language
          }, true)
            .then((data) => {
                requests++;
                this.data[this.categorys[i].name] = data;
                if (requests == this.categorys.length) {
                  resolve()
                }
              }
            )
            .catch(err => {
              reject(err)
            })
        }
      })
    })
  }

  /**
   get all categories from server
   will store all categories in the categories variable as array
   **/
  getCategory() {
    return new Promise((resolve, reject) => this.server.get("get-course-categories/", true)
      .then(data => {
          this.categorys = data;
          resolve(data);
        }
      )
      .catch(err => {
        reject(err);
      }))
  }

  /**
   returns promise and resolve if this course exists.
   Loads the courses if current not loaded.
   **/
  contains(id: number) {
    return new Promise((resolve, reject) => {
      if (this.data == null) {
        this.load().then(() => {
            let value = this.get(id);
            if (value) {
              resolve(value);
            }
            else {
              reject();
            }
          }
        )
          .catch(() => {
            reject()
          })
      }
      else {
        let value = this.get(id);
        if (value) {
          resolve(value);
        }
        else {
          reject();
        }
      }
    })
  }

  /**
   Returns the course by id
   **/
  get(id: number) {
    for (let i = 0; i < this.categorys.length; i++) {
      for (let j = 0; j < this.data[this.categorys[i].name].length; j++) {
        if (this.data[this.categorys[i].name][j]['id'] == Number(id)) {
          return this.data[this.categorys[i].name][j];
        }

      }
    }

    return false;
  }

  /**
   Returns all courses that a user has started already
   @author Claas Voelcker
   **/
  get_started() {
    let courses = [];
    for (let i = 0; i < this.categorys.length; i++) {
      for (let j = 0; j < this.data[this.categorys[i].name].length; j++) {
        if (this.data[this.categorys[i].name][j]['num_answered'] > 0) {
          courses.push(this.data[this.categorys[i].name][j]);
        }
      }
    }
    return courses
  }

}
