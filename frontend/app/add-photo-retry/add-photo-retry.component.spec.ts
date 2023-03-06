import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddPhotoRetryComponent } from './add-photo-retry.component';

describe('AddPhotoRetryComponent', () => {
  let component: AddPhotoRetryComponent;
  let fixture: ComponentFixture<AddPhotoRetryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddPhotoRetryComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddPhotoRetryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
