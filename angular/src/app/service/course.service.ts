import { Injectable } from '@angular/core';

import { ServerService } from './server.service'

@Injectable()
export class CourseService {

  data: any
  categorys: any;

  constructor(private server: ServerService) {
  }

  getByCat(id: number){
    let value = [];
    if(this.data != null){
      for(let i = 0; i < this.data.length; i++){
        for(let j = 0; j < this.data[i].category.length; j++){
          if(this.data[i].category[j].id == id){
            value.push(this.data[i])
          }
        }
      }
    }
    return value;
  }

  load(){
    return new Promise((resolve, reject) => this.server.post("courses/", {"type":"", "category":"", "language":"en"}, true)
      .then(data => {
        this.data = data
        resolve()
        }
      )
      .catch(err => {
        reject(err)
      })
    )
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
    for(let i = 0; i < this.data.length; i++){
      if(this.data[i]['id'] == id){
        return this.data[i];
      }
    }

    return false;
  }

}
