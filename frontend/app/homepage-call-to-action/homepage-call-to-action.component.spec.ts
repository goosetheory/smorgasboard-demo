import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomepageCallToActionComponent } from './homepage-call-to-action.component';

describe('HomepageCallToActionComponent', () => {
  let component: HomepageCallToActionComponent;
  let fixture: ComponentFixture<HomepageCallToActionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HomepageCallToActionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HomepageCallToActionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
