import {TestBed, inject} from '@angular/core/testing';

import {UserService} from './user.service';

import {ServerService} from './server.service'
import {Router} from "@angular/router"
import {CookieService} from 'angular2-cookie/core';
import {Http} from '@angular/http';


describe('UserService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [UserService],
    });
  });

  // it('should be created', inject([UserService], (service: UserService) => {
  //   expect(service).toBeTruthy();
  // }));

  // it('not logged in', inject([UserService, CookieService], (user: UserService, cookie: CookieService) => {
  //   expect(user.login).toBeFalsy();
  //   user.loginUser('admin', 'test').then(() => {
  //       let token = cookie.get('token');
  //       //expect(token).toBeTruthy();
  //     })
  // }));
});
