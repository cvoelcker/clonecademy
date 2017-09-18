import {Component} from '@angular/core';
import {AddQuestionModuleComponent} from '../add-question/add-question.module'
import {slideIn} from '../../../animations';
import {MdDialog, MdDialogRef} from '@angular/material';

@Component({
  selector: 'app-add-info-youtube',
  templateUrl: './add-info-youtube.component.html',
  styleUrls: ['./add-info-youtube.component.scss'],
  animations: [slideIn],
})
/**
 @title: AddInformationYoutubeComponent
 @author: Claas Voelcker

 This component is used to add an information text with included youtube videos
 between questions.
 */
export class AddInformationYoutubeComponent extends AddQuestionModuleComponent {
  body = {
    text_field: '',
    url: '',
  };
  compInfo: string = 'Loading';

  constructor(public dialog: MdDialog) {
    super()
  }

  /**
   * saving the video builds a JSON for the database handler
   * @author Claas Voelcker
   * @param form
   * @returns {{type: string, text_field: string, url: string}}
   */
  save(form): any {
    this.form = form;
    return {
      type: 'info_text_youtube',
      text_field: this.body.text_field,
      url: this.body.url,
    };
  }
}
