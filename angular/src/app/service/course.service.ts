import {Injectable} from '@angular/core';

import {ServerService} from './server.service'
import {UserService} from './user.service';

@Injectable()
/**
 * A service to get all course related data
 *
 * @author Leonhard Wiedmann
 */
export class CourseService {

  // the courses
  data = {};
  // categories to filter the courses
  categorys: any;

  constructor(private server: ServerService, private user: UserService) {
  }

  /**
   load courses for all categories for the current user language
   after loading sorts course for every category in data variable
   @author Leonhard Wiedmann
   @returns Promise
   **/
  load() {
    return new Promise((resolve, reject) => {
      this.getCategory().then(() => {
        let requests = 0
        if (this.categorys.length <= 0){
          resolve()
          this.data = []
        }
        // load all courses and sort them in a array by there categories
        for (let i = 0; i < this.categorys.length; i++) {
          this.server.post('courses/', {
            'type': '',
            'category': this.categorys[i].name,
            'language': this.user.language
          }, true)
            .then((data) => {
                requests++;
                this.data[this.categorys[i].name] = data;
                if (requests === this.categorys.length) {
                  // if all courses are loaded end the promise successfully
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
   @author Leonhard Wiedmann
   @returns void
   **/
  getCategory() {
    return new Promise((resolve, reject) => this.server.get('get-course-categories/', true)
      .then(data => {
          this.categorys = data;
          resolve(data);
        }
      )
      .catch(err => {
        this.categorys = []
        reject(err);
      }))
  }

  /**
   returns promise and resolve if this course exists.
   Loads the courses if currently not loaded.
   @author Leonhard Wiedmann
   @returns a promise resolving the course
   @param id: number
   **/
  contains(id: number) {
    return new Promise((resolve, reject) => {
      // loads the course if the data is not in cache
      if (this.data == null) {
        this.load().then(() => {
            const value = this.get(id);
            if (value) {
              resolve(value);
            } else {
              reject();
            }
          }
        )
          .catch(() => {
            reject()
          })
      } else {
        const value = this.get(id);
        if (value) {
          resolve(value);
        } else {
          reject();
        }
      }
    })
  }

  /**
   Returns the course by the course id
   If the id does not exist it will return false
   @author Leonhard Wiedmann
   @param id: number
   @returns a loaded course
   **/
  get(id: number) {
    for (let i = 0; i < this.categorys.length; i++) {
      for (let j = 0; j < this.data[this.categorys[i].name].length; j++) {
        if (this.data[this.categorys[i].name][j]['id'] === Number(id)) {
          return this.data[this.categorys[i].name][j];
        }
      }
    }
    return false;
  }

  /**
   Returns all courses that a user has started already
   @author Claas Voelcker
   @returns all started courses by the user
   **/
  get_started(): {}[] {
    const courses = [];
    for (let i = 0; i < this.categorys.length; i++) {
      for (let j = 0; j < this.data[this.categorys[i].name].length; j++) {
        // checks if more then one and less then all questions were answered
        const num_answered = this.data[this.categorys[i].name][j]['num_answered'];
        const num_total = this.data[this.categorys[i].name][j]['num_questions'];
        if (num_answered > 0 && num_answered < num_total) {
          courses.push(this.data[this.categorys[i].name][j]);
        }
      }
    }
    return courses
  }

}
