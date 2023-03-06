import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BoardInstructionsComponent } from './board-instructions.component';

describe('BoardInstructionsComponent', () => {
  let component: BoardInstructionsComponent;
  let fixture: ComponentFixture<BoardInstructionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BoardInstructionsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BoardInstructionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
