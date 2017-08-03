import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class ServerService {

private baseUrl = '/api/'
  private format = '/?format=json';

  constructor(private http: Http) { }

  getData(type: string){
    return this.http.get(this.baseUrl + type + this.format)
                  .toPromise()
                  .then(response => response.json())
                  .catch(this.handleError);
  }

  private handleError(error: any) {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }

}
