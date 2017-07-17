import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-add-question-module',
  template: '<p>implement me</p>',
})
export class AddQuestionModule {

  form = null;

  answers: any;

  public save(form): any{
    return "nix";
  }

  public edit( answers: any){
    if(answers != null){
      this.answers = answers;
    }
  }
 }
