import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoveToScanComponent } from './love-to-scan.component';

describe('LoveToScanComponent', () => {
  let component: LoveToScanComponent;
  let fixture: ComponentFixture<LoveToScanComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LoveToScanComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LoveToScanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
