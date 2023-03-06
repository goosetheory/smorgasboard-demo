import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BoardTrialInfoComponent } from './board-trial-info.component';

describe('BoardTrialInfoComponent', () => {
  let component: BoardTrialInfoComponent;
  let fixture: ComponentFixture<BoardTrialInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BoardTrialInfoComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BoardTrialInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
