import {Component, OnInit, ViewChild} from '@angular/core';
import {MdDialog} from '@angular/material';
import {DeleteDialogComponent} from '../delete-dialog/delete-dialog.component'

import {ServerService} from '../../service/server.service';

import {Router} from '@angular/router'

@Component({
  selector: 'app-course-categories',
  templateUrl: './course-categories.component.html',
  styleUrls: ['./course-categories.component.sass']
})
export class CourseCategoriesComponent {

  loading = true;
  create = false;

  categoryname: string;
  categorycolor: string;
  categoryID: number;
  index: number = -1;

  categories: any;

  courses: any;

  error = false;
  errorMessage = '';

  dialogRef: any;

  edit = false;


  constructor(
    private server: ServerService,
    private router: Router,
    public dialog: MdDialog
  ) {
    // load the data for all categories
    this.server.get('get-course-categories/')
      .then(data => {
        this.categories = data;
        this.loading = false;
      })
  }

  change(c: any) {
    this.categoryname = c.name
    this.categorycolor = c.color
    this.categoryID = c.id
    this.index = this.categories.indexOf(c)
    this.create = false;
    this.edit = true;
  }

  openCreate() {
    this.categoryname = '';
    this.categorycolor = '';
    this.create = true;
    this.edit = true;
  }

  delete() {
    this.server.post('get-course-categories/', {delete: false, id: this.categoryID})
      .then(answer => {
        this.courses = answer;
        answer['id'] = this.categoryID
        const dialogRef = this.dialog.open(DeleteDialogComponent, {
          data: answer
        })
        dialogRef.afterClosed().subscribe( valid => {
          if (valid['deleted'] === true) {
            this.categories.splice(this.index, 1);
            this.edit = false

          }

        })
      })
  }

  // register the updated category
  register(value) {
    if (value.valid) {
      const data = value.value
      if (this.categoryID !== undefined && !this.create) {
        data['id'] = this.categoryID;
      }
      this.server.post('get-course-categories/', data)
        .then(answer => {
          if (this.create) {
            this.categories.push(answer)
            this.change(this.categories[this.categories.length - 1])
          } else {
            this.categories[this.index] = answer
          }
        })
        .catch(errorRes => {
          this.error = true;
          this.errorMessage = errorRes;
        })
    }
  }

}
;
/*
 @Component({
 selector: 'app-course-categories',
 templateUrl: './delete-dialog.html',
 styleUrls: ['./course-categories.component.sass']
 })
 export class DialogContentDeleteDialogComponent {}
 */
