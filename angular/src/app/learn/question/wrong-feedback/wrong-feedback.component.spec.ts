import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { NgModule } from '@angular/core';


import { BaseTest } from '../../../../base-test';

import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';

import { LoaderComponent } from '../../loader/loader.component';
import {MdDialog, MdDialogModule, MdDialogRef } from '@angular/material';
import { ErrorMessageComponent } from './wrong-feedback.component';

@NgModule({
    declarations: [WrongFeedbackComponent],
    entryComponents: [WrongFeedbackComponent],
    imports: [new BaseTest().imports()],
    exports: [WrongFeedbackComponent],
})
class TestModule { }

describe('ErrorMessageComponent', () => {

  let dialog: MdDialog;
  let component: WrongFeedbackComponent;
  let fixture: ComponentFixture<ErrorMessageComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
      TestBed.configureTestingModule({
      imports: [ base.imports(), TestModule,  MdDialogModule ]
    })
    TestBed.overrideModule(
      BrowserDynamicTestingModule, {
        set: {
          entryComponents: [WrongFeedbackComponent]
        }
      }
    )
    .compileComponents();
  }));

  beforeEach(() => {
        dialog = TestBed.get(MdDialog);
        let dialogRef = dialog.open(WrongFeedbackComponent);

        component = dialogRef.componentInstance;
    });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
