import {Component, OnInit} from '@angular/core';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-add-question-module',
  template: '<p>implement me</p>',
})
export class AddQuestionModule {

  form = null;

  body: any;

  public save(form): any {
    return "nix";
  }

  public edit(body: any) {
    if (body != null) {
      this.body = body;
      if (this.body['url'] != undefined) {
        this.body['url'] = 'https://www.youtube.com/embed/' + this.body['url']
      }
    }
  }
}
