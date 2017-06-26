import { Component } from '@angular/core';
import {TranslateService} from '@ngx-translate/core';

import { UserService } from './service/user.service'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'Clonecademy';

  constructor(private user: UserService, private translate: TranslateService){
    translate.setDefaultLang('en');
    translate.use('en');
  }

}
