import { Component, OnInit, ViewChild, ViewContainerRef } from '@angular/core';
import { Http, RequestOptions, Headers } from '@angular/http';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-static-page',
  templateUrl: './static-page.component.html',
  styleUrls: ['./static-page.component.sass']
})
export class StaticPageComponent implements OnInit {
  data: any;

  constructor(public http: Http, public router: Router, public route: ActivatedRoute) { }

  ngOnInit() {
    this.route.params.subscribe(data => {
      this.get(data.page + ".html")
    })
  }

  get(site: string){
    this.http.get('/assets/statics/' + site)
      .toPromise()
      .then(data => this.data = data)
      .catch(err => {console.log(err), this.router.navigate(['404']) })
  }

}
