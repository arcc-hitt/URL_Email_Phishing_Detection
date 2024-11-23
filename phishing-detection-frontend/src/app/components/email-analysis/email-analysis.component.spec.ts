import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmailAnalysisComponent } from './email-analysis.component';

describe('EmailAnalysisComponent', () => {
  let component: EmailAnalysisComponent;
  let fixture: ComponentFixture<EmailAnalysisComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmailAnalysisComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EmailAnalysisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
