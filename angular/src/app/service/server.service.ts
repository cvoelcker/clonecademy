import { Injectable } from '@angular/core';
import { Http, RequestOptions, Headers } from '@angular/http';
import { HttpModule } from '@angular/http';

import {CookieService} from 'angular2-cookie/core';
import {MdDialog, MdDialogRef} from '@angular/material';
import {Observable} from 'rxjs/Rx';

import { ErrorDialog } from '../service/error.service'

import { LoaderComponent } from '../loader/loader.component';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class ServerService {

  private baseUrl = 'http://0.0.0.0:8000/'

  headers = new Headers({'Accept': 'application/json', 'Content-Type': 'application/json'});

  private token: string;

  private loader: MdDialogRef<LoaderComponent>


  constructor(private http: Http, private cookie: CookieService, private dialog: MdDialog, private error: ErrorDialog) {
    this.token = this.cookie.get("token")
  }

  private makeHeader(){
    // the jwt token is the string given from django after login
    return new Headers({'Authorization': "JWT " + this.cookie.get("token"), 'Accept': 'application/json', 'Content-Type': 'application/json'});

  }

  // call this function to get data from the server
  // the token will be passed
  // if silent is true the loader will not be shown
  get(type: string, silent = false, error = true){
    let loader;
    if(!silent){
      loader = this.dialog.open(LoaderComponent, {
        disableClose: true
      })
    }


    let options = new RequestOptions({headers: this.makeHeader()})
    return new Promise((resolve, reject) => this.http.get(this.baseUrl + type, options)
      .toPromise()
      .then(response => {
        if(!silent){
          loader.close()
        }
        resolve(response.json())
      })
      .catch(err => {
        if(!silent){
          loader.close()
        }
        if(error){
          this.handleError(err, this.error)
        }
        reject(err)
      })
    )
  }

  // call this function to get data from the server
  // if silent is true the loader will not be shown
  post(type: string, body: any, silent = false, error = true){
    let loader;
    if(!silent){

      loader = this.dialog.open(LoaderComponent, {
        disableClose: true
      })
    }

    body = JSON.stringify(body)
    //this.headers.append('Authorization', 'Token ' + this.token)
    let options = new RequestOptions({headers: this.makeHeader()})

    return new Promise((resolve, reject) => this.http.post(this.baseUrl + type, body, options)
                  .toPromise()
                  .then(response => {
                    if(!silent){
                      loader.close()
                    }
                    resolve(response.json())
                  })
                  .catch(err => {
                    if(!silent){
                      loader.close()
                    }
                    if(error){
                      this.handleError(err, this.error)
                    }
                    reject(err)
                  })
                )
  }

  // error handler will show a popup with the error Message
  private handleError(error: any, dialog) {
    console.error('An error occurred', error);
    dialog.open(error.statusText || error.message)
    return Promise.reject(error.message || error);
  }

  // sends request to server and saves the token from server as cookie for future requests
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
