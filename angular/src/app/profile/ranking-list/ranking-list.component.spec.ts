import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {BaseTest} from '../../base-test';


import {RankingListComponent} from './ranking-list.component';

describe('RankingListComponent', () => {
  let component: RankingListComponent;
  let fixture: ComponentFixture<RankingListComponent>;

  beforeEach(async(() => {
    const base = new BaseTest();
    TestBed.configureTestingModule({
      declarations: [RankingListComponent],
      imports: [base.imports()],
      providers: [base.providers()]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RankingListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
