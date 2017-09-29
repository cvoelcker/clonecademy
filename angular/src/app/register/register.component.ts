import {Component, OnInit} from '@angular/core';

import {ServerService} from '../service/server.service';
import {UserService} from '../service/user.service';

import {ErrorDialog} from '../service/error.service'

import {FormGroup, FormControl, Validators, FormBuilder} from '@angular/forms';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.sass']
})
export class RegisterComponent {

  languages: Array<{ id: string, name: string }> = [{
    id: 'en',
    name: 'English'
  }, {id: 'de', name: 'Deutsch'}]

  /*
  variables for register
  */
  newUsername: string;
  newEmail: string;
  newPassword: string;
  newPassword2: string;
  newFirstName = '';
  newLastName = '';
  newAge = -1;

  public registerForm = new FormGroup({
    email: new FormControl('email', Validators.email),
    username: new FormControl('username', Validators.required),
    password: new FormControl('password', Validators.required),
    language: new FormControl('language', Validators.required)
  })

  constructor(
    private error: ErrorDialog,
    private server: ServerService,
    private fb: FormBuilder,
    private user: UserService
  ) {
  }

  // register a new user.
  register(value) {
    if (value.valid && value.value['password'] === value.value['password2']) {
      const data = value.value
      delete data['password2'];
      data['groups'] = [];
      data['profile'] = {};
      this.server.post('register/', data, false, false)
        .then(answer => {
          this.user.loginUser(this.newUsername, this.newPassword)
        })
    }

  }

}
