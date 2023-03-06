import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomepageUsesComponent } from './homepage-uses.component';

describe('HomepageUsesComponent', () => {
  let component: HomepageUsesComponent;
  let fixture: ComponentFixture<HomepageUsesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HomepageUsesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HomepageUsesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
