import { TestBed } from '@angular/core/testing';

import { AddPhotoLinkService } from './add-photo-link.service';

describe('AddPhotoLinkService', () => {
  let service: AddPhotoLinkService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AddPhotoLinkService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
