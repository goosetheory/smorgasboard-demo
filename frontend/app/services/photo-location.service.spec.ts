import { TestBed } from '@angular/core/testing';

import { PhotoLocationService } from './photo-location.service';

describe('PhotoLocationService', () => {
  let service: PhotoLocationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PhotoLocationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
