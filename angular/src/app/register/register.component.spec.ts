import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import {TranslateModule, TranslateLoader} from '@ngx-translate/core';

import {TranslateHttpLoader} from '@ngx-translate/http-loader';
import {MdDialog, MdDialogModule, MdButtonModule, MdAutocompleteModule, MdCheckboxModule, MdTooltipModule, MdCardModule, MdInputModule, MdSelectModule, MaterialModule, MdTabsModule, MdProgressSpinnerModule} from '@angular/material';
import { FormsModule } from '@angular/forms';
import { ServerService } from '../service/server.service';
import { UserService } from '../service/user.service';

import { HttpModule, Http } from '@angular/http';

import { ErrorDialog } from "../service/error.service"

import { RegisterComponent } from './register.component';

function createTranslateLoader(http: Http) {
    return new TranslateHttpLoader(http, './assets/lang/', '.json');
}

describe('RegisterComponent', () => {
  let component: RegisterComponent;
  let fixture: ComponentFixture<RegisterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        TranslateModule.forRoot({
          loader: {
            provide: TranslateLoader,
            useFactory: (createTranslateLoader),
            deps: [Http]
          }
        }),
        FormsModule,
        MdButtonModule,
        MdCheckboxModule,
        MdInputModule,
        MdSelectModule,
        MdTabsModule,
        MdDialogModule,
        MdCardModule,
        MdTooltipModule,
        MdAutocompleteModule,
        MdProgressSpinnerModule,
        HttpModule
      ],
      providers: [
        ErrorDialog,
        ServerService,
        UserService
      ],
      declarations: [ RegisterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
