import { Component } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

import { UserService } from './service/user.service'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'CloneCademy';

  constructor(private user: UserService, private translate: TranslateService) {
    translate.addLangs(['en', 'de']);
    translate.setDefaultLang('en');
    translate.use('en');
  }
  changeLang(lang: string) {
    this.translate.use(lang);
  }

}
