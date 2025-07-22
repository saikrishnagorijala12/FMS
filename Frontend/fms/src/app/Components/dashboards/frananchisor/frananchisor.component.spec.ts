import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FrananchisorComponent } from './frananchisor.component';

describe('FrananchisorComponent', () => {
  let component: FrananchisorComponent;
  let fixture: ComponentFixture<FrananchisorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FrananchisorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FrananchisorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
