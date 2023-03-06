import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JoinBoardComponent } from './join-board.component';

describe('JoinBoardComponent', () => {
  let component: JoinBoardComponent;
  let fixture: ComponentFixture<JoinBoardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ JoinBoardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(JoinBoardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
