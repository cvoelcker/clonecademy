import { Component, OnInit } from '@angular/core';

import { ServerService } from '../service/server.service';
import { UserService } from '../service/user.service';
import { LoginComponent } from '../login/login.component';

import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.sass']
})
export class RegisterComponent {

  constructor(private server: ServerService, private fb: FormBuilder, private user: UserService){

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
  newGroup: string = "";
  invalidRegister: boolean;
  errorMessage: string;


  ngOnInit() {
  }


  public registerForm = new FormGroup({
    email: new FormControl("email", Validators.email),
    username: new FormControl('username', Validators.required),
    password: new FormControl('password', Validators.required)
  })

  register(value){
    console.log(value.value)

    if(value.valid && value.value["password"] === value.value['password2']){
      let data = value.value
      delete data['password2']
      this.server.post("register/", data)
        .then(answer => {
          console.log(answer)
          this.user.loginUser(this.newUsername, this.newPassword)
        })
        .catch(error => {
          this.invalidRegister = true;
          this.errorMessage = error.statusText
        });
    }
    else{
      console.log("false")
    }

  }

}
