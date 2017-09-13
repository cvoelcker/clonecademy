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

  public registerForm = new FormGroup({
    email: new FormControl("email", Validators.email),
  })

  // validated entered email and post request if valid
  submit(form){
    if(form.valid){
      let data = form.value;
      this.server.post("pw_reset/", data, false, false)
        .then(answer => {
          this.answer = answer;
          console.log("a normal answer")
          console.log(answer)
        })
        .catch(err => {
          console.log("catched!")
          let dialogRef = this.errorDialog.open("stay");
          console.log("should have opened this by now")
        })
    }
  }

}
