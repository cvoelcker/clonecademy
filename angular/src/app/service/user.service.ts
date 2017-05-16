import { Injectable } from '@angular/core';

@Injectable()
export class UserService {

  id: number;
  name: string;

  constructor() {
    //this.id = 1;
  }

  loggedIn(): boolean {
    return this.id != null
  }

}
