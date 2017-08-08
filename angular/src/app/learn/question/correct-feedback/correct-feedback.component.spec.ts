import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { NgModule } from '@angular/core';


import { BaseTest } from '../../../../base-test';

import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';

import { LoaderComponent } from '../../../loader/loader.component';
import {MdDialog, MdDialogModule, MdDialogRef } from '@angular/material';
import { CorrectFeedbackComponent } from './correct-feedback.component';

@NgModule({
    declarations: [CorrectFeedbackComponent],
    entryComponents: [CorrectFeedbackComponent],
    imports: [new BaseTest().imports()],
    exports: [CorrectFeedbackComponent],
})
class TestModule { }

describe('CorrectFeedbackComponent', () => {

  let dialog: MdDialog;
  let component: CorrectFeedbackComponent;
  let fixture: ComponentFixture<CorrectFeedbackComponent>;

  beforeEach(async(() => {
    let base = new BaseTest();
      TestBed.configureTestingModule({
      imports: [ base.imports(), TestModule,  MdDialogModule ]
    })
    TestBed.overrideModule(
      BrowserDynamicTestingModule, {
        set: {
          entryComponents: [CorrectFeedbackComponent]
        }
      }
    )
    .compileComponents();
  }));

  beforeEach(() => {
        dialog = TestBed.get(MdDialog);
        let dialogRef = dialog.open(CorrectFeedbackComponent);

        component = dialogRef.componentInstance;
    });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
