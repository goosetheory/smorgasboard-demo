import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomepageCardsComponent } from './homepage-cards.component';

describe('HomepageCardsComponent', () => {
  let component: HomepageCardsComponent;
  let fixture: ComponentFixture<HomepageCardsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HomepageCardsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HomepageCardsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
