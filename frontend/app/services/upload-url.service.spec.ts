import { TestBed } from '@angular/core/testing';

import { UploadUrlService } from './upload-url.service';

describe('UploadUrlService', () => {
  let service: UploadUrlService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UploadUrlService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
