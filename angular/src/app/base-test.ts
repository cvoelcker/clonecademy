import {TranslateModule, TranslateLoader} from '@ngx-translate/core';

import {TranslateHttpLoader} from '@ngx-translate/http-loader';
import {
  MdSidenavModule,
  MdMenuModule,
  MdDialog,
  MdDialogModule,
  MdButtonModule,
  MdAutocompleteModule,
  MdCheckboxModule,
  MdTooltipModule,
  MdCardModule,
  MdInputModule,
  MdSelectModule,
  MaterialModule,
  MdTabsModule,
  MdProgressSpinnerModule
} from '@angular/material';
import {FormsModule} from '@angular/forms';
import {ReactiveFormsModule} from '@angular/forms';
import {RouterTestingModule} from '@angular/router/testing';

import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

import {ErrorMessageComponent} from './error-message/error-message.component';

import {LoaderComponent} from './loader/loader.component';

import {ServerService} from './service/server.service';
import {UserService} from './service/user.service';
import {CourseService} from './service/course.service';

import {MarkdownModule} from 'angular2-markdown';

import {HttpModule, Http} from '@angular/http';

import {ErrorDialog} from './service/error.service'

import {CookieService} from 'angular2-cookie/services/cookies.service';

function createTranslateLoader(http: Http) {
  return new TranslateHttpLoader(http, './assets/lang/', '.json');
}

export class BaseTest {

  public imports(array?: Array<any>): Array<any> {
    const base = [TranslateModule.forRoot({
      loader: {
        provide: TranslateLoader,
        useFactory: (createTranslateLoader),
        deps: [Http]
      }
    }),
      MarkdownModule.forRoot(),
      FormsModule,
      MdButtonModule,
      MdCheckboxModule,
      MdInputModule,
      MdSelectModule,
      MdTabsModule,
      MdDialogModule,
      MdCardModule,
      MdTooltipModule,
      MdAutocompleteModule,
      MdProgressSpinnerModule,
      MdMenuModule,
      HttpModule,
      MdSidenavModule,
      ReactiveFormsModule,
      RouterTestingModule,
      BrowserAnimationsModule]
    if (array != null) {
      for (let i = 0; i < array.length; i++) {
        base.push(array[i])
      }
    }
    return base;
  }

  public providers(array?: Array<any>): Array<any> {
    const data = [ErrorDialog, ServerService, UserService, CookieService, CourseService];
    if (array != null) {
      for (let i = 0; i < array.length; i++) {
        data.push(array[i]);
      }
    }
    return data;
  }

  public entryComponents(array?: Array<any>): Array<any> {
    const data = [ErrorMessageComponent, LoaderComponent]
    if (array != null) {
      for (let i = 0; i < array.length; i++) {
        data.push(array[i])
      }
    }
    return data;
  }
}
