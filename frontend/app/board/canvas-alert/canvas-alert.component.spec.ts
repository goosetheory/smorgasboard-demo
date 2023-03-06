import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CanvasAlertComponent } from './canvas-alert.component';

describe('CanvasAlertComponent', () => {
  let component: CanvasAlertComponent;
  let fixture: ComponentFixture<CanvasAlertComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CanvasAlertComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CanvasAlertComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
