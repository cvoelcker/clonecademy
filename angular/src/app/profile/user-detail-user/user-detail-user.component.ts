import {Component, Input} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router'
import {UserService} from '../../service/user.service';
import {ServerService} from '../../service/server.service';
import {ProfilePageComponent} from '../profile-page/profile-page.component';
import {ErrorDialog} from '../../service/error.service'
import {FormGroup, FormControl, Validators, FormBuilder} from '@angular/forms';
import {ImageCropperDialogComponent} from '../../image-cropper/image-cropper.component';
import {AuthDialogComponent} from './auth-dialog/auth-dialog.component'

import {TranslateService} from '@ngx-translate/core';

import {MdDialog, MdDialogRef} from '@angular/material';



/*
'Profile' of the user.
Used to change profilefields
*/
@Component({
  selector: 'app-user-detail-user',
  templateUrl: './user-detail-user.component.html',
  styleUrls: ['./user-detail-user.component.scss']
})
export class UserDetailUserComponent {
  languages: Array<{ id: string, name: string }> = [{
    id: 'en',
    name: 'English'
  }, {id: 'de', name: 'Deutsch'}]
  // {username: string, id: number, email: string, group: {}, dateRegistered: Date, dateString: string}

  body = {
    avatar: '',
  }

  constructor(private user: UserService,
              private server: ServerService,
              private translate: TranslateService,
              public dialog: MdDialog, ) {
  }
  /*
  is called when the form to edit the profile is submitted
  @author Tobias Huber
  */
  edit(value) {
    if (value.valid && value.value['password'] === value.value['password2']) {
      const formData = value.value
      if (this.body['avatar'] !== '') {
        formData['avatar'] = this.body['avatar']
      }

      const dialogRef = this.dialog.open(AuthDialogComponent, {
        data: formData, });
    } else {
      console.log('form not valid')
    }
  }

  /*
  opens the image upload dialog, called by 'upload avatar'
  */
  openImageDialog(width: number, height: number, key: string) {
    const dialogRef = this.dialog.open(ImageCropperDialogComponent, {
      data: {
        width: width,
        height: height
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.body[key] = result
      }
    });
  }
}
