import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomepageHowItWorksComponent } from './homepage-how-it-works.component';

describe('HomepageHowItWorksComponent', () => {
  let component: HomepageHowItWorksComponent;
  let fixture: ComponentFixture<HomepageHowItWorksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HomepageHowItWorksComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HomepageHowItWorksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
