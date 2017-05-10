import { Component, OnInit } from '@angular/core';
import { ServerService } from '../server.service';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit {

  data: any[];
  error: any;

  constructor( private server: ServerService) { }

  getData(){
    this.server
    .getData('polls')
    .then(data => this.data = data)
    .catch(error => this.error = error);
  }

  ngOnInit() {
    this.getData();
  }

}
