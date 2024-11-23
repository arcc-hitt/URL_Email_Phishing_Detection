import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PhishingLogComponent } from './phishing-log.component';

describe('PhishingLogComponent', () => {
  let component: PhishingLogComponent;
  let fixture: ComponentFixture<PhishingLogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PhishingLogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PhishingLogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
