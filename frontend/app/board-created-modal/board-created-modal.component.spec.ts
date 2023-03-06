import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BoardCreatedModalComponent } from './board-created-modal.component';

describe('BoardCreatedModalComponent', () => {
  let component: BoardCreatedModalComponent;
  let fixture: ComponentFixture<BoardCreatedModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BoardCreatedModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BoardCreatedModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
