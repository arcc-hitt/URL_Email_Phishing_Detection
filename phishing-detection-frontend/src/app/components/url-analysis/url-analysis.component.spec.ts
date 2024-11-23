import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UrlAnalysisComponent } from './url-analysis.component';

describe('UrlAnalysisComponent', () => {
  let component: UrlAnalysisComponent;
  let fixture: ComponentFixture<UrlAnalysisComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UrlAnalysisComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UrlAnalysisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
