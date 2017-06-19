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
        console.log("test")
        resolve()
        }
      )
      .catch(err => {
        reject(err)
      })
    )
  }

  contains(id: number){
    return new Promise((resolve, reject) => {
      if(this.data == null){
        this.load().then(() => {
            if(this.check(id)){
              resolve();
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
        if(this.check(id)){
          resolve();
        }
        else{
          reject();
        }
      }
    })



  }

  private check(id: number){
    for(let i = 0; i < this.data.length; i++){
      if(this.data[i]['id'] == id){
        return true;
      }
    }

    return false;
  }

}
