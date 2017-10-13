import { Component, OnInit } from '@angular/core';

import { ServerService } from '../../service/server.service';
import { Settings } from '../../injectible/page.injectible'

@Component({
  selector: 'app-page-settings',
  templateUrl: './page-settings.component.html',
  styleUrls: ['./page-settings.component.sass'],
})
export class PageSettingsComponent implements OnInit {

  private settings: any;

  constructor(private server: ServerService, private sett: Settings) {
    server.post('settings/edit/', {})
      .then((data: any) => {
        this.settings = data
      })
  }

  ngOnInit() {
  }

  fileChangeListener($event) {
    const file: File = $event.target.files[0];
    const myReader: FileReader = new FileReader();
    const that = this;
    myReader.onloadend = function (loadEvent: any) {

      that.settings.image = loadEvent.target.result
    };
    myReader.readAsDataURL(file);
  }

  save(f) {
    if (f.valid) {
      this.server.post('settings/edit/', this.settings)
        .then(data => {
          this.sett.load()
          console.log(data)
        })
    }
  }

}
