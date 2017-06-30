import { Component, OnInit } from '@angular/core';

import { ServerService } from '../service/server.service';
import { UserService } from '../service/user.service';

import { ErrorDialog } from "../service/error.service"

import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.sass']
})
export class RegisterComponent {

  constructor(
    private error: ErrorDialog,
    private server: ServerService,
    private fb: FormBuilder,
    private user: UserService
  ){
  }

  /*
  variables for register
  TODO: refactor name and surname to first and last name
   */
  newUsername: string;
  newEmail: string;
  newPassword: string;
  newPassword2: string;
  newFirstName: string = "";
  newLastName: string = "";
  newAge: number = -1;


  ngOnInit() {
  }


  public registerForm = new FormGroup({
    email: new FormControl("email", Validators.email),
    username: new FormControl('username', Validators.required),
    password: new FormControl('password', Validators.required)
  })

  // register a new user.
  register(value){
    if(value.valid && value.value["password"] === value.value['password2']){
      let data = value.value
      delete data['password2']
      this.server.post("register/", data)
        .then(answer => {
          this.user.loginUser(this.newUsername, this.newPassword)
        })
    }
    else{
      if(!value.valid){
        this.error.open("Email, username and password is required")
      }
      else{
        this.error.open("The password is not matching")
      }

    }

  }

}
