import {TestBed, inject} from '@angular/core/testing';

import {BaseTest} from '../base-test';


import {ServerService} from './server.service';

describe('ServerService', () => {
  beforeEach(() => {
    const base = new BaseTest();
    TestBed.configureTestingModule({
      imports: [base.imports()],
      providers: [base.providers([ServerService])],
    });
  });

  it('should be created', inject([ServerService], (service: ServerService) => {
    expect(service).toBeTruthy();
  }));
});
