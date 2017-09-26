import {Component, OnInit} from '@angular/core';

import {QuestionModuleComponent} from '../question/question.module'
import {SafeResourceUrl} from '@angular/platform-browser';
import {ActivatedRoute} from '@angular/router'
import {DomSanitizer} from '@angular/platform-browser';

/**
 View a Youtube Video as question
 @author Class Voelcker
**/
@Component({
  selector: 'app-information-text',
  templateUrl: './info-youtube.component.html',
  styleUrls: ['./info-youtube.component.scss']
})
export class InformationYoutubeComponent extends QuestionModuleComponent implements OnInit {

  url: SafeResourceUrl

  ngOnInit() {
    this.set_video_url()
  }

  /**
   * Builds the url and circumvents sanitation (actual sanitation is done before saving the url to database)
   * @author Claas Voelcker
   * @returns {SafeResourceUrl} a sanitized utb url
   */
  set_video_url() {
    const url = 'https://www.youtube.com/embed/' + this.data['url'] + '?rel=0&amp;showinfo=0'
    this.url = this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }

  // return array of the marked answers
  submit(): any {
    return true;
  }
}
