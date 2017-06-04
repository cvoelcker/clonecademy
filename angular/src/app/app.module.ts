import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { RouterModule, Routes } from '@angular/router';
import { CookieService } from 'angular2-cookie/services/cookies.service';

import { ServerService } from './service/server.service';

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

import { AddQuestionModule } from "./add-question/add-question.module"
import { QuestionModule } from "./question/question.module";

const appRoutes: Routes = [
  { path: 'dashboard', component: DashboardComponent },
  { path: 'login',      component: LoginComponent },
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'course/:id',
    component: CourseComponent,
  },
  {
    path: "course/:id/:module",
    component: ModuleComponent,
  },
  {
    path: "course/:id/:module/:question",
    component: QuestionComponent,
  },
  {
    path: "createCourse",
    component: CreateCourseComponent
  },
  {
    path: "profile/statistics",
    component: StatisticsComponent
  },
  { path: '**', component: PageNotFoundComponent }
];


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
  ],
  imports: [
    RouterModule.forRoot(appRoutes),
    BrowserModule,
    FormsModule,
    HttpModule,
  ],
  providers: [ServerService, CookieService],
  bootstrap: [
    AppComponent,
  ],
  entryComponents: [
    AddModuleComponent,
    AddQuestionModule,
    AddQuestionComponent,
    AddMultiplyChoiceComponent,
    // you have to add all modules for questions here
    MultipleChoiceQuestionComponent
  ]
})
export class AppModule { }
