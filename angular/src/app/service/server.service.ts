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

  getBaseUrl(){
    return this.baseUrl;
  }

  private loader: MdDialogRef<LoaderComponent>

  constructor(private http: Http, private cookie: CookieService, private dialog: MdDialog, private error: ErrorDialog) {
  }

  private makeHeader(){
    // the jwt token is the string given from django after login
    return new Headers({'Authorization': "Token " + this.cookie.get("token"), 'Accept': 'application/json', 'Content-Type': 'application/json'});
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

    let options = new RequestOptions({headers: this.makeHeader()})

    return new Promise((resolve, reject) => this.http.post(this.baseUrl + type, body, options)
                  .toPromise()
                  .then(response => {
                    if(!silent){
                      loader.close()
                    }

                    try{
                      response = response.json()

                    } catch(e){
                    }
                    resolve(response)

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
          this.cookie.put("token", response.token);
          this.cookie.put("username", name);
          resolve(response);
        },
        (err) => {
          reject(err.json())
        }))
  }

  downloadStatistics(request = {}){
    request['format'] = 'csv'
    this.post("user/statistics", request)
    .then(data => {
      // create the file to download
      let blob = new Blob([data["_body"]], {type: "text/csv"});
      let downloadData = URL.createObjectURL(blob)
      // create a button which will be clicked to download
      // at the moment it looks like this is the only workaround for a download dialog
      var anchor = document.createElement("a");
      // set download name
      anchor.download = "statistics.csv";
      anchor.href = downloadData;
      // hide button
      anchor.setAttribute('visibility', "hidden")
      anchor.setAttribute("display", "none")
      // add button to body, activate the download and remove the button again
      document.body.appendChild(anchor)
      anchor.click();
      document.body.removeChild(anchor)
    })
  }

}
