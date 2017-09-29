import {Component, AfterViewInit, ChangeDetectorRef} from '@angular/core';

@Component({
  selector: 'app-loader',
  templateUrl: './loader.component.html',
  styleUrls: ['./loader.component.scss']
})
export class LoaderComponent implements AfterViewInit {

  constructor(private _changeDetectionRef: ChangeDetectorRef) {
  }

  ngAfterViewInit() {
    this._changeDetectionRef.detectChanges()
  }

}
