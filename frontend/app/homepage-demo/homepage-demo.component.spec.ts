import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomepageDemoComponent } from './homepage-demo.component';

describe('HomepageDemoComponent', () => {
  let component: HomepageDemoComponent;
  let fixture: ComponentFixture<HomepageDemoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HomepageDemoComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HomepageDemoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
