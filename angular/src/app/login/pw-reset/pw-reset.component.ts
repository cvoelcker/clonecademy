import { Component } from '@angular/core';

import { ServerService } from '../../service/server.service';
import { UserService } from '../../service/user.service';

import { ErrorDialog } from "../../service/error.service"

import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';

@Component({
  selector: 'login-pw-reset',
  templateUrl: './pw-reset.component.html',
  styleUrls: ['./pw-reset.component.sass']
})
export class PwResetComponent {

  languages: Array<{id: string, name: string}> = [{id: "en", name: "English"}, {id: "de", name: "Deutsch"}]


  constructor(
    private error: ErrorDialog,
    private server: ServerService,
    private fb: FormBuilder,
    private user: UserService
  ){
  }

  /*
  e-mail address for reset
   */
  newEmail: string;
  answer: any;
  loading: boolean;

  public registerForm = new FormGroup({
    email: new FormControl("email", Validators.email),
  })

  // register a new user.
  submit(form){
    if(form.valid){
      let data = form.value;
      console.log(data);
      this.loading = true;
      this.server.post("pw_reset/", data, false, false)
        .then(answer => {
          this.answer = answer;
        })
        .catch(err => {
          console.log(err)
        })
    }
  }

}
