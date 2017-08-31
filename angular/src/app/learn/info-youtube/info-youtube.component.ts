import {Component} from '@angular/core';

import {QuestionModule} from '../question/question.module'
import {SafeResourceUrl} from '@angular/platform-browser';

@Component({
  selector: 'app-InformationText',
  templateUrl: './info-youtube.component.html',
  styleUrls: ['./info-youtube.component.scss']
})
export class InformationYoutubeComponent extends QuestionModule {

  /**
   * Builds the url and circumvents sanitation (actual sanitation is done before saving the url to database)
   * @author Claas Voelcker
   * @returns {SafeResourceUrl} a sanitized utb url
   */
  get_video_url(): SafeResourceUrl {
    let url = "https://www.youtube.com/embed/" + this.data["url"] + "?rel=0&amp;showinfo=0"
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }

  // return array of the marked answers
  submit(): any {
    return true;
  }
}
