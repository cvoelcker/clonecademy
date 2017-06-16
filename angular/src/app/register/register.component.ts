import { Component, OnInit } from '@angular/core';

import { ServerService } from '../service/server.service';
import { LoginComponent } from '../login/login.component'

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.sass']
})
export class RegisterComponent extends LoginComponent{

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

  register(){
    if (this.newPassword !== this.newPassword2)
      return -1;
    let newUserInfo = {
      username: this.newUsername,
      email: this.newEmail,
      password: this.newPassword,
      first_name: this.newFirstName,
      last_name: this.newLastName,
			age: this.newAge,
			group: this.newGroup,
    };
    this.server.post("register/", newUserInfo)
      .then(answer => {
        console.log(answer)
        this.username = this.newUsername;
        this.password = this.newPassword
        this.login()
      })
      .catch(error => {
        this.invalidRegister = true;
        this.errorMessage = error.statusText
      });
  }

}
