import { TestBed, inject } from '@angular/core/testing';

import { ErrorDialog } from './error.service';

describe('ErrorService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ErrorDialog]
    });
  });

  // it('should be created', inject([ErrorDialog], (service: ErrorDialog) => {
  //   expect(service).toBeTruthy();
  // }));
});
