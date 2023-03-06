import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BoardStartModalComponent } from './board-start-modal.component';

describe('BoardStartModalComponent', () => {
  let component: BoardStartModalComponent;
  let fixture: ComponentFixture<BoardStartModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BoardStartModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BoardStartModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
