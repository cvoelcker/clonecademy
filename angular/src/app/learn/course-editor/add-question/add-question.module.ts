import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-add-question-module',
  template: '<p>implement me</p>',
})
export class AddQuestionModule {

  form = null;
  question: string;

  answers: any;

  public save(form): any{
    return "nix";
  }

  public edit(questionBody: string, answers: any){
    if(questionBody != null){
      this.question = questionBody;
    }
    if(answers != null){
      this.answers = answers;
    }
  }
 }
