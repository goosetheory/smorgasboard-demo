import { TestBed } from '@angular/core/testing';

import { BoardMembershipService } from './board-membership.service';

describe('BoardMembershipService', () => {
  let service: BoardMembershipService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BoardMembershipService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
