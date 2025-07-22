import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FranchiseeComponent } from './franchisee.component';

describe('FranchiseeComponent', () => {
  let component: FranchiseeComponent;
  let fixture: ComponentFixture<FranchiseeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FranchiseeComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FranchiseeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
