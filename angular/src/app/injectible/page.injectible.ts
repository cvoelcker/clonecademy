import {Injectable} from '@angular/core';
import {CanActivate, Router} from '@angular/router';
import {ServerService} from '../service/server.service';


@Injectable()
export class Settings {

  loaded = false;

  data = {name: '', image: ''}

  constructor(private server: ServerService) {
    this.load()
  }

  load() {
    this.server.get('settings')
      .then((response: any) => {
        this.data = response
        this.loaded = true
      })
  }
}
