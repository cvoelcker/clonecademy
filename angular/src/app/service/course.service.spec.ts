import {TestBed, inject} from '@angular/core/testing';

import {BaseTest} from '../base-test';
import {CourseService} from './course.service';

let simpleData = {
  general: [
    {
      category: 'general',
      difficulty: 1,
      id: 1,
      language: 'en',
      name: 'title',
      num_answered: 0,
      num_questions: 2,
      responsible_mod: 1,
      modules: [
        {
          id: 1,
          learning_text: "module learning Text",
          name: "module Title",
          questions: [
            {
              body: "question body",
              solved: false,
              last_module: true,
              last_question: true,
              type: 'info_text',
              question_body: {
                text_field: "text",
                img: ""
              }
            },
            {
              body: "question body",
              solved: false,
              last_module: true,
              last_question: true,
              type: 'info_text',
              question_body: {
                text_field: "text",
                img: ""
              }
            }
          ]
        }
      ]
    }
  ]
}

let categories = [{name: 'general'}]

describe('CourseService', () => {
  beforeEach(() => {
    let base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [base.imports()],
      providers: [base.providers([CourseService])],
    });
  });

  it('should be created', inject([CourseService], (service: CourseService) => {
    expect(service).toBeTruthy();
  }));

  it('test get', inject([CourseService], (service: CourseService) => {
    service.categorys = categories
    service.data = simpleData
    expect(service.get(1)['name']).toBe("title")
  }));

  it('test started', inject([CourseService], (service: CourseService) => {
    service.data = simpleData
    service.categorys = categories
    expect(service.get_started().length).toBe(0)
    service.data['general'][0]['num_answered'] = 1
    expect(service.get_started().length).toBe(1)
  }))
});
