import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {NgModule} from '@angular/core';


import {BaseTest} from '../base-test';

import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';

import {LoaderComponent} from '../loader/loader.component';
import {MdDialog, MdDialogModule, MdDialogRef} from '@angular/material';
import {ErrorMessageComponent} from './error-message.component';

@NgModule({
  declarations: [ErrorMessageComponent],
  entryComponents: [ErrorMessageComponent],
  imports: [new BaseTest().imports()],
  exports: [ErrorMessageComponent],
})
class TestModule {
}

describe('ErrorMessageComponent', () => {

  let dialog: MdDialog;
  let component: ErrorMessageComponent;
  const fixture: ComponentFixture<ErrorMessageComponent>;

  beforeEach(async(() => {
    const base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [base.imports(), TestModule, MdDialogModule]
    })
    TestBed.overrideModule(
      BrowserDynamicTestingModule, {
        set: {
          entryComponents: [ErrorMessageComponent]
        }
      }
    )
      .compileComponents();
  }));

  beforeEach(() => {
    dialog = TestBed.get(MdDialog);
    const dialogRef = dialog.open(ErrorMessageComponent);

    component = dialogRef.componentInstance;
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
