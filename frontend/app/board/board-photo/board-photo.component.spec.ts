import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BoardPhotoComponent } from './board-photo.component';

describe('BoardPhotoComponent', () => {
  let component: BoardPhotoComponent;
  let fixture: ComponentFixture<BoardPhotoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BoardPhotoComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BoardPhotoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
