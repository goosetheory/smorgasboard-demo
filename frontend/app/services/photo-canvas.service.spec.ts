import { TestBed } from '@angular/core/testing';

import { PhotoCanvasService } from './photo-canvas.service';

describe('PhotoCanvasService', () => {
  let service: PhotoCanvasService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PhotoCanvasService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
