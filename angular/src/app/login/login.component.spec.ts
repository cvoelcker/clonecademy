import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ErrorDialog } from "../service/error.service"

import { UserService } from '../service/user.service';
import { Router } from "@angular/router";
import { ServerService } from '../service/server.service'

import { CookieService } from 'angular2-cookie/core';

import { LoginComponent } from './login.component';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LoginComponent, ErrorDialog, UserService, Router, ServerService ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
