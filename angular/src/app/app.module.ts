import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpModule, Http } from '@angular/http';

// translate Module
import {TranslateModule, TranslateLoader} from '@ngx-translate/core';
import {TranslateHttpLoader} from '@ngx-translate/http-loader';

//markdown
import { MarkdownModule } from 'angular2-markdown';

// Material Style
import {MdSidenavModule, MdDialog, MdDialogModule, MdIconModule, MdMenuModule, MdButtonModule, MdAutocompleteModule, MdCheckboxModule, MdTooltipModule, MdCardModule, MdInputModule, MdSelectModule, MaterialModule, MdTabsModule, MdProgressSpinnerModule} from '@angular/material';

import {ImageCropperComponent, CropperSettings} from 'ng2-img-cropper';

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
import { DashboardComponent } from './learn/dashboard/dashboard.component';
import { LoggedInDirective } from './directive/logged-in.directive';
import { MenuComponent } from './menu/menu.component';
import { CourseComponent } from './learn/course/course.component';
import { QuestionSidenavComponent } from './learn/question-sidenav/question-sidenav.component';

import { QuestionDictionary } from './learn/question-dictionary';

import { ModuleDirective } from './directive/module.directive';
import { QuestionComponent } from './learn/question/question.component';
// course editor
import { CreateCourseComponent } from './learn/course-editor/create-course/create-course.component';
import { AddModuleComponent } from './learn/course-editor/add-module/add-module.component';
import { AddQuestionComponent } from './learn/course-editor/add-question/add-question.component';
import { AddQuestionModule } from "./learn/course-editor/add-question/add-question.module"

import { StatisticsComponent } from './profile/personal_statistics/statistics.component';
import { RequestModComponent } from './profile/request-mod/request-mod.component';
import { QuestionModule } from "./learn/question/question.module";
import { ProfilesComponent } from './admin/profiles/profiles.component';
import { UserDetailComponent } from './admin/user-detail/user-detail.component';
import { UserDetailUserComponent } from './profile/user-detail-user/user-detail-user.component'
import { ProfilePageComponent } from './profile/profile-page/profile-page.component';
import { AdminPageComponent } from './admin/admin-page/admin-page.component';
import { RegisterComponent } from './register/register.component';
import { ErrorMessageComponent } from './error-message/error-message.component';
import { WrongFeedbackComponent } from './learn/question/wrong-feedback/wrong-feedback.component';
import { LoaderComponent } from './loader/loader.component';
import { EditCourseComponent } from './learn/course-editor/create-course/edit-course.component';
import { StaticPageComponent } from './static-page/static-page.component';
import { ImageCropperDialogComponent } from "./image-cropper/image-cropper.component";

// Viewing started courses on the welcome page
import { CourseViewComponent } from "./learn/view-courses/view-courses.component";
import { FooterMainpageComponent } from './footer-mainpage/footer-mainpage.component';
import { QuizQuestionComponent } from './quiz/quiz-question/quiz-question.component';


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
       path: "",
       component: CourseViewComponent,
     },
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
       component: CourseComponent,
     },
     {
       path: "edit/:id",
       component: EditCourseComponent
     }
   ]
  },
  {
    path: "course/quiz/:id/:quiz",
    component: QuizQuestionComponent
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
        path: "details",
        component: UserDetailUserComponent,
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
        children: [
          {
            path: ":id",
            component: UserDetailComponent
          }
        ]
      }
    ]
  },
  {
    path: "404",
    component: PageNotFoundComponent,
  },
  {
    path: ':page',
    component: StaticPageComponent
  },
];

export function createTranslateLoader(http: Http) {
    return new TranslateHttpLoader(http, './assets/lang/', '.json');
}

let QuestionList = QuestionDictionary.questionComponents

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent,
    PageNotFoundComponent,
    LoggedInDirective,
    MenuComponent,
    CourseComponent,
    ModuleDirective,
    QuestionComponent,
    CreateCourseComponent,
    AddModuleComponent,
    AddQuestionComponent,
    StatisticsComponent,
    QuestionModule,
    QuestionList,
    AddQuestionModule,
    ProfilesComponent,
    UserDetailComponent,
    RequestModComponent,
    ProfilePageComponent,
    AdminPageComponent,
    RegisterComponent,
    ErrorMessageComponent,
    WrongFeedbackComponent,
    LoaderComponent,
    EditCourseComponent,
    UserDetailUserComponent,
    ImageCropperDialogComponent,
    ImageCropperComponent,
    StaticPageComponent,
    CourseViewComponent,
    FooterMainpageComponent,
    QuestionSidenavComponent,
    QuizQuestionComponent,
  ],
  imports: [
    BrowserAnimationsModule,
    RouterModule.forRoot(appRoutes),
    FormsModule,
    TranslateModule.forRoot({
      loader: {
        provide: TranslateLoader,
        useFactory: (createTranslateLoader),
        deps: [Http]
      }
    }),
    MarkdownModule.forRoot(),
    ReactiveFormsModule,
    BrowserModule,
    HttpModule,
    MdButtonModule,
    MdCheckboxModule,
    MdInputModule,
    MdSelectModule,
    MdTabsModule,
    MdDialogModule,
    MdCardModule,
    MdTooltipModule,
    MdSidenavModule,
    MdAutocompleteModule,
    MdProgressSpinnerModule,
    MdMenuModule,
    MdIconModule,
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
    ErrorMessageComponent,
    WrongFeedbackComponent,
    LoaderComponent,
    CourseComponent,
    CreateCourseComponent,
    ImageCropperDialogComponent,
    // profile page components
    StatisticsComponent,
    RequestModComponent,
    UserDetailComponent,
    // admin Page components
    ProfilesComponent,
    // you have to add all modules for questions here
    QuestionList,
    CourseViewComponent,
  ]
})
export class AppModule { }
