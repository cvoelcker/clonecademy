import {
  Component,
  ComponentRef,
  ViewChild,
  ViewContainerRef,
  ComponentFactoryResolver,
  ComponentFactory,
  EventEmitter,
  Output,
  AfterViewInit
} from '@angular/core';
import {MdDialog, MdDialogRef} from '@angular/material';
import {AddModuleComponent} from '../add-module/add-module.component'
import {Router, ActivatedRoute} from '@angular/router'
import {ImageCropperDialogComponent} from '../../../image-cropper/image-cropper.component';

import {menuSlideIn, slideIn} from '../../../animations'

import {FormGroup, FormControl, Validators, FormBuilder} from '@angular/forms';

import {CourseService} from '../../../service/course.service'
import {UserService} from '../../../service/user.service'

import {ServerService} from '../../../service/server.service'
@Component({
  selector: 'app-create-course',
  templateUrl: './create-course.component.html',
  styleUrls: ['./create-course.component.scss'],
  animations: [menuSlideIn, slideIn]
})
export class CreateCourseComponent implements AfterViewInit {

  @ViewChild('modules', {read: ViewContainerRef}) modules: ViewContainerRef;
  childComponent: ComponentFactory<AddModuleComponent>;
  moduleArray: ComponentRef<AddModuleComponent>[] = [];
  length = 0;
  error = false;

  loading = true;
  loadCourse: boolean;

  quiz: Array<{
    invisible: boolean,
    question: string,
    image: string,
    answers: Array<{
      text: string,
      img: string,
      correct: boolean
    }>
  }> = [];


    languages: Array<{ id: string, name: string }> = [{
      id: 'en',
      name: 'English'
    }, {id: 'de', name: 'Deutsch'}]
    lng: string;
    categories: {};
    category: number;
    description: string;

    difficultys: Array<{ value: number, name: string }> = [
      {value: 0, name: 'Easy'},
      {value: 1, name: 'moderate'},
      {value: 2, name: 'difficult'},
      {value: 3, name: 'expert'}
    ]

    diff: number;
    title: string;

    public courseForm = new FormGroup({
      title: new FormControl('title', Validators.required),
      category: new FormControl('category', Validators.required),
    })

    constructor(
      public router: Router,
      public route: ActivatedRoute,
      public server: ServerService,
      private componentFactory: ComponentFactoryResolver,
      private course: CourseService,
      private user: UserService,
      private fb: FormBuilder,
      public dialog: MdDialog
    ) {
      this.childComponent = this.componentFactory.resolveComponentFactory(AddModuleComponent)
      this.server.get('get-course-categories/', true)
        .then(data => {
          this.categories = data;
          this.loading = false;
        })
    }

  /***
   create a basic quiz with 5 questions and every question has 4 possible answers
   @author: Leonhard Wiedmann
   ***/
  createQuiz() {
    this.quiz = []
    for (let i = 0; i < 5; i++) {
      this.quiz.push({
        question: '',
        invisible: true,
        image: '',
        answers: [
          {
            text: '',
            img: '',
            correct: false
          },
          {
            text: '',
            img: '',
            correct: false
          },
          {
            text: '',
            img: '',
            correct: false
          },
          {
            text: '',
            img: '',
            correct: false
          }
        ]
      })
    }
  }

  /***
   creates a simple quiz question with 4 answers
   @author: Leonhard Wiedmann
   ***/
  addQuizQuestion() {
    this.quiz.push({
      question: '',
      image: '',
      invisible: true,
      answers: [
        {
          text: '',
          img: '',
          correct: false
        },
        {
          text: '',
          img: '',
          correct: false
        },
        {
          text: '',
          img: '',
          correct: false
        },
        {
          text: '',
          img: '',
          correct: false
        }
      ]
    })
  }

  /***
   open a dialog for to upload a image
   @author: Leonhard Wiedmann
   ***/
  openImageDialog(width: number, height: number, questionKey: number, answerKey: number = -1) {
    const dialogRef = this.dialog.open(ImageCropperDialogComponent, {
      data: {
        width: width,
        height: height
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        if (answerKey !== -1) {
          this.quiz[questionKey].answers[answerKey].img = result
        } else {
          this.quiz[questionKey].image = result
        }
      }
    });
  }

  setCourseTrue(b: boolean) {
    this.loadCourse = b
  }

  setCategory(id: number) {
    this.category = id;
  }

  setLanguage(id: string) {
    this.lng = id
  }

  setDifficulty(id: number) {
    this.diff = id
  }

  setDescription(value: string) {
    this.description = value;
  }

  setTitle(title: string) {
    this.title = title;
  }


  ngAfterViewInit() {
  }

  clearModule() {
    this.modules.clear();
    this.moduleArray = [];
  }

  addModule(id?: number, title?: string, moduleDescription?: string, questions?: Array<any>) {
    const moduleComponent = this.modules.createComponent(this.childComponent);
    const module = (<AddModuleComponent> moduleComponent.instance)

    module.id = id

    if (title !== undefined) {
      module.title = title
    }
    if (moduleDescription !== undefined) {
      module.learningText = moduleDescription
    }
    if (questions !== undefined) {
      for (let i = 0; i < questions.length; i++) {
        const question = questions[i]
        module.editQuestion(question)
      }
    }
    this.moduleArray.push(moduleComponent)

    module.clear.subscribe((data) => {
      const moduleSingle = moduleComponent
      if (data === 'remove') {
        this.moduleArray.splice(this.moduleArray.indexOf(moduleSingle), 1)
        moduleSingle.destroy();
      } else if (data === 'up') {
        const index = this.modules.indexOf(moduleComponent.hostView);
        const i = index - 1 > 0 ? index - 1 : 0;
        this.modules.move(moduleComponent.hostView, i);
      } else if (data === 'down') {
        const index = this.modules.indexOf(moduleComponent.hostView);
        const i = index + 1 < this.moduleArray.length ? index + 1 : this.moduleArray.length - 1;
        this.modules.move(moduleComponent.hostView, i);
      }
    })
  }

  removeCourse() {
    this.modules.detach(0)
  }

  save(f) {
    if (f.valid) {
      const saveModules = this.saveModules(f)
      for (const q of this.quiz) {
        delete q.invisible;
      }
      const course = {
        name: f.value['title'],
        difficulty: f.value['difficulty'],
        language: f.value['language'],
        category: f.value['category'],
        modules: saveModules,
        quiz: this.quiz,
        description: this.description
      };
      this.uploadState(course);
    }
  }

  saveModules(form) {
    const saveModules = [];
    for (let i = 0; i < this.moduleArray.length; i++) {
      const module = this.moduleArray[i];
      const index = this.modules.indexOf(module.hostView);
      const m = (<AddModuleComponent> module.instance).save(form);
      m['order'] = index
      saveModules.push(m)
    }
    return saveModules
  }

  uploadState(course) {
    this.server.post('courses/save', course)
      .then(data => {
        this.course.load()
        this.router.navigate(['/course'])
      })
      .catch(err => {})
  }


}
