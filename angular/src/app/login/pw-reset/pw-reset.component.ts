import { Component } from '@angular/core';
import { ErrorDialog } from "../../service/error.service";
import { ServerService } from '../../service/server.service';
import { UserService } from '../../service/user.service';

import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-pw-reset',
  templateUrl: './pw-reset.component.html',
  styleUrls: ['./pw-reset.component.sass']
})
export class PwResetComponent {

  languages: Array<{id: string, name: string}> = [{id: "en", name: "English"}, {id: "de", name: "Deutsch"}]


  constructor(
    private errorDialog: ErrorDialog,
    private server: ServerService,
    private fb: FormBuilder,
  ){
  }

  /*
  e-mail address for reset
   */
  newEmail: string;
  answer: any;
  loading: boolean;
  error: boolean;
  data: any;

  public registerForm = new FormGroup({
    email: new FormControl("email", Validators.email),
  })

  // validated entered email and post request if valid
  submit(form){
    if(form.valid){
      this.data = form.value;
      this.server.post("pw_reset/", this.data, false, false)
        .then(answer => {
          this.answer = answer;
        })
        .catch(err => {
          this.error = true;
          this.errorDialog.open("THIS OPENED IN CATCH");
          console.log(this.error);
        })
    } else {
      this.errorDialog.open("did ypouu try this?")
    }
  }

}
