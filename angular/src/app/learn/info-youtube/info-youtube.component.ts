import {Component} from '@angular/core';

import {QuestionModule} from '../question/question.module'
import {SafeResourceUrl} from '@angular/platform-browser';

@Component({
  selector: 'app-InformationText',
  templateUrl: './info-youtube.component.html',
  styleUrls: ['./info-youtube.component.scss']
})
export class InformationYoutubeComponent extends QuestionModule {

  data: {};

  get_video_url(): SafeResourceUrl {
    console.log(this.data["url"])
    return this.sanitizer.bypassSecurityTrustResourceUrl(this.data["url"]);
  }

  // return array of the marked answers
  submit(): any {
    return true;
  }
}
