import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  username: {text: string, valid: boolean};
  password: {text: string, valid: boolean};
  submitted: boolean;

  constructor() {
  }

  login(){
    //this.submitted = true;
    console.log("tests")
  }
  ngOnInit() {
  }

}
