import { TestBed } from '@angular/core/testing';

import { PhotoWebsocketService } from './photo-websocket.service';

describe('PhotoWebsocketService', () => {
  let service: PhotoWebsocketService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PhotoWebsocketService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
