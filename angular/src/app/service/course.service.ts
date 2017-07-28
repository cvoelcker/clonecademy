import { Injectable } from '@angular/core';

import { ServerService } from './server.service'
import { UserService } from './user.service';

@Injectable()
export class CourseService {

  data = {};
  categorys: any;

  constructor(private server: ServerService, private user: UserService) {
  }


  load(){
    return new  Promise((resolve, reject) => {
      this.getCategory().then(() => {
        for( let i = 0; i < this.categorys.length; i++){
          this.server.post("courses/", {"type":"", "category":this.categorys[i].name, "language": this.user.language}, true)
          .then((data) => {
            this.data[this.categorys[i].name] = data
            if(i == this.categorys.length -1){
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

  getCategory(){
    return new Promise((resolve, reject) => this.server.get("get-course-categories/", true)
    .then(data => {
        this.categorys = data
        resolve(data)
      }
    )
    .catch(err => {
        reject(err);
      }))
  }

  contains(id: number){
    return new Promise((resolve, reject) => {
      if(this.data == null){
        this.load().then(() => {
          let value = this.get(id)
            if(value){
              resolve(value);
            }
            else{
              reject();
            }
          }
        )
        .catch(() => {
          reject()
        })
      }
      else{
        let value = this.get(id)
        if(value){
          resolve(value);
        }
        else{
          reject();
        }
      }
    })



  }


  get(id: number){
    for(let i = 0; i < this.categorys.length; i++){
      for(let j = 0; j < this.data[this.categorys[i].name].length; j++){
        if(this.data[this.categorys[i].name][j]['id'] == Number(id)){
          return this.data[this.categorys[i].name][j];
        }

      }
    }

    return false;
  }

}
