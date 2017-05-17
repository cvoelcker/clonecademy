import { Injectable } from '@angular/core';
import { Http, RequestOptions, Headers } from '@angular/http';

import {CookieService} from 'angular2-cookie/core';

import {Observable} from 'rxjs/Rx';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class ServerService {

  private baseUrl = 'http://0.0.0.0:8000/'
  private format = '?format=json';

  private token: string;

  constructor(private http: Http, private cookie: CookieService) {
    this.token = this.cookie.get('token')
  }

  getData(type: string){
    return this.http.get(this.baseUrl + type + this.format)
                  .toPromise()
                  .then(response => response.json())
                  .catch(this.handleError);
  }

  setToken(token: string){
    this.token = token;
  }

  private handleError(error: any) {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }

  public login(name: string, password: string){

    let body = JSON.stringify({username: name, password: password}); // Stringify payload
    let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
    let options = new RequestOptions({headers: headers})

    return new Promise((resolve, reject) => this.http.post(this.baseUrl + "api-auth", body, options)
      .subscribe(
        (res) => {
          let response = res.json();
          this.token = response
          this.cookie.put("token", response);
          resolve(true)
        },
        (err) => {
          reject(false)
        }))
  }

}

export class User{
  token: string;
  non_field_errors: string;
}
