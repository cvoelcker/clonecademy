import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule, Http } from '@angular/http';

// translate Module
import {TranslateModule, TranslateLoader} from '@ngx-translate/core';
import {TranslateHttpLoader} from '@ngx-translate/http-loader';

// Material Style
import {MdButtonModule, MdCheckboxModule, MdInputModule, MdSelectModule, MaterialModule, MdTabsModule, MdProgressSpinnerModule} from '@angular/material';

import {MdDialog, MdDialogModule} from '@angular/material';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { ReactiveFormsModule } from '@angular/forms';

import { RouterModule, Routes } from '@angular/router';
import { CookieService } from 'angular2-cookie/services/cookies.service';

import { ServerService } from './service/server.service';
import { UserService } from './service/user.service';
import { CourseService } from './service/course.service'
import { ErrorDialog } from "./service/error.service";

import { Admin } from "./injectible/admin.injectible"

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LoggedInDirective } from './directive/logged-in.directive';
import { MenuComponent } from './menu/menu.component';
import { CourseComponent } from './course/course.component';
import { ModuleComponent } from './module/module.component';
import { MultipleChoiceQuestionComponent } from './multiple-choice-question/multiple-choice-question.component';
import { ModuleDirective } from './directive/module.directive';
import { QuestionComponent } from './question/question.component';
import { CreateCourseComponent } from './create-course/create-course.component';
import { AddMultiplyChoiceComponent } from './add-multiply-choice/add-multiply-choice.component';
import { AddModuleComponent } from './add-module/add-module.component';
import { AddQuestionComponent } from './add-question/add-question.component';
import { StatisticsComponent } from './personal_statistics/statistics.component';
import { RequestModComponent } from './request-mod/request-mod.component';
import { AddQuestionModule } from "./add-question/add-question.module"
import { QuestionModule } from "./question/question.module";
import { ProfilesComponent } from './profiles/profiles.component';
import { UserDetailComponent } from './user-detail/user-detail.component';
import { ProfilePageComponent } from './profile-page/profile-page.component';
import { AdminPageComponent } from './admin-page/admin-page.component';
import { RegisterComponent } from './register/register.component';
import { ErrorMessageComponent } from './error-message/error-message.component';
import { LoaderComponent } from './loader/loader.component';

const appRoutes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'course',
   component: DashboardComponent,
   children: [
     {
       path: "create_course",
       component: CreateCourseComponent,
     },
     {
       path:"page_not_found",
       component: PageNotFoundComponent,
     },
     {
       path: ":id",
       component: CourseComponent
     }
   ]
  },
  {
    path: "course/:id/:module/:question",
    component: QuestionComponent,
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'register',
    component: RegisterComponent
  },
  {
    path: "profile",
    component: ProfilePageComponent,
    children: [
      {
        path: "",
        redirectTo: "details",
        pathMatch: "full"
      },
      {
        path: "details",
        component: UserDetailComponent,
      },
      {
        path: "request_mod",
        component: RequestModComponent,
      },
      {
        path: "statistics",
        component: StatisticsComponent,
      }
  ]
  },
  {
    path: "admin",
    component: AdminPageComponent,
    canActivate: [
      Admin
    ],
    children: [
      {
        path: "profiles",
        component: ProfilesComponent,
      }
    ]
  },
  {
    path: "404",
    component: PageNotFoundComponent,
  },
  {
    path: '**',
    redirectTo: "404",
  }
];

export function createTranslateLoader(http: Http) {
    return new TranslateHttpLoader(http, './assets/lang/', '.json');
}

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent,
    PageNotFoundComponent,
    LoggedInDirective,
    MenuComponent,
    CourseComponent,
    ModuleComponent,
    MultipleChoiceQuestionComponent,
    ModuleDirective,
    QuestionComponent,
    CreateCourseComponent,
    AddMultiplyChoiceComponent,
    AddModuleComponent,
    AddQuestionComponent,
    StatisticsComponent,
    QuestionModule,
    AddQuestionModule,
    ProfilesComponent,
    UserDetailComponent,
    RequestModComponent,
    ProfilePageComponent,
    AdminPageComponent,
    RegisterComponent,
    ErrorMessageComponent,
    LoaderComponent,
  ],
  imports: [
    RouterModule.forRoot(appRoutes),
    TranslateModule.forRoot({
      loader: {
        provide: TranslateLoader,
        useFactory: (createTranslateLoader),
        deps: [Http]
      }
    }),
    ReactiveFormsModule,
    BrowserModule,
    FormsModule,
    HttpModule,
    MdButtonModule,
    MdCheckboxModule,
    MdInputModule,
    MdSelectModule,
    MdTabsModule,
    MdDialogModule,
    MdProgressSpinnerModule,
    BrowserAnimationsModule,
  ],
  exports: [
  ],
  providers: [
    ServerService,
    UserService,
    CourseService,
    CookieService,
    MdDialog,
    ErrorDialog,
    Admin
  ],
  bootstrap: [
    AppComponent,
  ],
  entryComponents: [
    AddModuleComponent,
    AddQuestionModule,
    AddQuestionComponent,
    AddMultiplyChoiceComponent,
    ErrorMessageComponent,
    LoaderComponent,
    CourseComponent,
    CreateCourseComponent,
    // profile page components
    StatisticsComponent,
    RequestModComponent,
    UserDetailComponent,
    // admin Page components
    ProfilesComponent,
    // you have to add all modules for questions here
    MultipleChoiceQuestionComponent
  ]
})
export class AppModule { }
