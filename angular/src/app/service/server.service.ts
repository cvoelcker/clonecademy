import { Injectable } from '@angular/core';
import { Http, RequestOptions, Headers } from '@angular/http';

import {CookieService} from 'angular2-cookie/core';
import {MdDialog} from '@angular/material';
import {Observable} from 'rxjs/Rx';

import { ErrorDialog } from '../service/error.service'

import { LoaderComponent } from '../loader/loader.component';


import 'rxjs/add/operator/toPromise';

@Injectable()
export class ServerService {

  private baseUrl = 'http://0.0.0.0:8000/'

  headers = new Headers({'Accept': 'application/json', 'Content-Type': 'application/json'});

  private token: string;


  constructor(private http: Http, private cookie: CookieService, private dialog: MdDialog, private error: ErrorDialog) {
    this.token = this.cookie.get("token")
  }

  private makeHeader(){
    // the jwt token is the string given from django after login
    return new Headers({'Authorization': "JWT " + this.cookie.get("token"), 'Accept': 'application/json', 'Content-Type': 'application/json'});

  }

  get(type: string){

    let loader = this.dialog.open(LoaderComponent, {
      disableClose: true
    })

    let options = new RequestOptions({headers: this.makeHeader()})
    return this.http.get(this.baseUrl + type, options)
      .toPromise()
      .then(res => {
        loader.close()
        return res.json()
      })
      .catch(err => {
        loader.close()
        this.handleError(err, this.error)
      })
  }

  post(type: string, body: any){

    let loader = this.dialog.open(LoaderComponent, {
      disableClose: true
    })

    body = JSON.stringify(body)
    //this.headers.append('Authorization', 'Token ' + this.token)
    let options = new RequestOptions({headers: this.makeHeader()})

    return this.http.post(this.baseUrl + type, body, options)
                  .toPromise()
                  .then(response => {
                    loader.close()
                    return response.json()
                  })
                  .catch(err => {
                    loader.close()
                    this.handleError(err, this.error)
                  });
  }

  private handleError(error: any, dialog) {
    console.error('An error occurred', error);
    dialog.open(error.statusText || error.message)
    return Promise.reject(error.message || error);
  }

  public login(name: string, password: string){

    let headers = new Headers({ 'Accept': 'application/json', 'Content-Type': 'application/json'});

    let body = JSON.stringify({username: name, password: password}); // Stringify payload

    let options = new RequestOptions({headers: headers})

    return new Promise((resolve, reject) => this.http.post(this.baseUrl + "api-auth/", body, options)
      .subscribe(
        (res) => {
          let response = res.json();
          this.token = response.token
          this.cookie.put("token", response.token);
          this.cookie.put("username", name);
          resolve(response);
        },
        (err) => {
          reject(err.json())
        }))
  }

  public register(username: string, password: string, email: string, firstName: string, lastName:string, ) {
    /** TODO: implement ??? or maybe not ???
     * check wether or not the function in app.component.ts is sufficient
     */
  }

  public clearToken(){
    this.token = null;
  }

  public getToken(){
    return this.token;
  }

}

export class User{
  token: string;
  non_field_errors: string;
}
