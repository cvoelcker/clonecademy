import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {NgModule} from '@angular/core';


import {BaseTest} from '../base-test';

import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';

import {LoaderComponent} from '../loader/loader.component';
import {MdDialog, MdDialogModule, MdDialogRef} from '@angular/material';
import {QuizEndPopupComponent} from './quiz-end-popup.component';

@NgModule({
  declarations: [QuizEndPopupComponent],
  entryComponents: [QuizEndPopupComponent],
  imports: [new BaseTest().imports()],
  exports: [QuizEndPopupComponent],
})
class TestModule {
}

describe('QuizEndPopupComponent', () => {

  let dialog: MdDialog;
  let component: QuizEndPopupComponent;
  const fixture: ComponentFixture<QuizEndPopupComponent>;

  beforeEach(async(() => {
    const base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [base.imports(), TestModule, MdDialogModule]
    })
    TestBed.overrideModule(
      BrowserDynamicTestingModule, {
        set: {
          entryComponents: [QuizEndPopupComponent]
        }
      }
    )
      .compileComponents();
  }));

  beforeEach(() => {
    dialog = TestBed.get(MdDialog);
    const dialogRef = dialog.open(QuizEndPopupComponent);

    component = dialogRef.componentInstance;
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
