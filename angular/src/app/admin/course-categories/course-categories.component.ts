import { Component, OnInit, ViewChild } from '@angular/core';
import { MdDialog } from '@angular/material';
import { DeleteDialogComponent } from '../delete-dialog/delete-dialog.component'

import { ServerService } from '../../service/server.service';

import { Router } from "@angular/router"

@Component({
  selector: 'app-course-categories',
  templateUrl: './course-categories.component.html',
  styleUrls: ['./course-categories.component.sass']
})
export class CourseCategoriesComponent implements OnInit {

  loading = true;
  create = false;

  selected: any;

  categories: any;

  courses: any;

  error = false;
  errorMessage = "";



  constructor(private server: ServerService, private router: Router,
              public dialog: MdDialog) { }

  ngOnInit() {
    // load the data for all categories

    this.server.get("get-course-categories/", true)
      .then(data => {
        this.categories = data;
        this.loading = false;
      })
  }

  change(c: any){
    this.selected = c;
    this.create = false;
    console.log("change called")
  }

  openCreate(){
    console.log("open create called")
    this.create = true;
  }

  delete(){
    console.log("delete init")
    this.server.post('courses/', {"category":this.selected.name, "type":"",
    "language":""}, false, false)
      .then(answer => {
        this.courses = answer;
      })


    const dialogRef = this.dialog.open(DeleteDialogComponent, {
      height: '350px',
      data: this.courses
    });
    console.log('dialog opened')

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
    console.log('got result')

    /*
    this.server.post('get-course-categories/',{
      "delete": "true",
      "id": this.selected.id}
    )*/
  }




  // register the updated category
  register(value){
    console.log(value)
    if (value.valid) {
      let data = value.value
      if (data['categorycolor']=='')
        delete data['categorycolor'];
      if (data['categoryname']=='')
        delete data['categoryname'];
      if (this.selected != undefined && !this.create) {
        data["id"] = this.selected.id;
      }
      this.server.post('get-course-categories/', data, false, false)
        .then(answer => {
          this.selected = answer;
          this.categories.push(answer);
        })
        .catch(errorRes => {
          this.error = true;
          this.errorMessage=errorRes;
        })
      if (this.create) {
        this.change(this.selected)
      }
    }
  }

};
/*
@Component({
  selector: 'app-course-categories',
  templateUrl: './delete-dialog.html',
  styleUrls: ['./course-categories.component.sass']
})
export class DialogContentDeleteDialogComponent {}
*/
