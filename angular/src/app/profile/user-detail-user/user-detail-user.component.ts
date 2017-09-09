import {Component, OnInit, Input} from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router'
import { UserService } from '../../service/user.service';
import { ServerService } from '../../service/server.service';
import { ProfilePageComponent } from '../profile-page/profile-page.component';
import { ErrorDialog } from "../../service/error.service"
import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';

import {TranslateService} from '@ngx-translate/core';

import {MdDialog, MdDialogRef} from '@angular/material';

import { ImageCropperDialogComponent } from '../../image-cropper/image-cropper.component';


@Component({
  selector: 'app-user-detail-user',
  templateUrl: './user-detail-user.component.html',
  styleUrls: ['./user-detail-user.component.scss']
})

export class UserDetailUserComponent {
  languages: Array<{id: string, name: string}> = [{id: "en", name: "English"}, {id: "de", name: "Deutsch"}]
  // {username: string, id: number, email: string, group: {}, dateRegistered: Date, dateString: string}

  body = {
    avatar: '',
  }

  constructor(
    private user: UserService,
    private server: ServerService,
    private translate: TranslateService,
    public dialog: MdDialog,
    ) {}

    ngOnInit() {
      }

    edit(value){



      if(value.valid && value.value["password"] === value.value['password2']){
        let data = value.value
        console.log(data);
        data["avatar"] = this.body["avatar"]
        this.user.edit(data)
      }
    }

    openImageDialog(width: number, height: number, key: string){
      let dialogRef = this.dialog.open(ImageCropperDialogComponent, {
        data: {
          width: width,
          height: height
        }
      });
      dialogRef.afterClosed().subscribe(result => {
        if(result){
          this.body[key] = result
        }
      });
    }
  }
