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
        console.log(data)
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
