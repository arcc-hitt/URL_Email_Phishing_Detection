import { Component, OnDestroy, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snack-bar';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { Subject, takeUntil, finalize } from 'rxjs';

import { PhishingLogService } from '../phishing-log/phishing-log.service';
import { environment } from '../../../environments/environment';

interface AnalysisResult {
  autoencoder_score: number;
  xgboost_score: number;
  is_phishing: boolean;
}

@Component({
  selector: 'app-url-analysis',
  standalone: true,
  imports: [
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    ReactiveFormsModule,
    CommonModule,
    MatIconModule,
    MatSnackBarModule,
    NgxChartsModule
  ],
  templateUrl: './url-analysis.component.html',
  styleUrls: ['./url-analysis.component.scss']
})
export class UrlAnalysisComponent implements OnDestroy {
  private readonly destroy$ = new Subject<void>();
  private readonly http = inject(HttpClient);
  private readonly fb = inject(FormBuilder);
  private readonly phishingLogService = inject(PhishingLogService);
  private readonly snackBar = inject(MatSnackBar);

  urlForm: FormGroup = this.fb.group({
    url: ['', [
      Validators.required, 
      Validators.pattern(/^https?:\/\/(?:[-\w.])+(?:\:[0-9]+)?(?:\/(?:[\w\/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$/)
    ]]
  });

  loading = false;
  analysisResult: AnalysisResult | null = null;
  chartData: Array<{ name: string; value: number }> = [];
  view: [number, number] = [700, 400];
  error: string | null = null;

  get urlControl() {
    return this.urlForm.get('url');
  }

  onSubmit(): void {
    if (!this.urlForm.valid) {
      this.urlForm.markAllAsTouched();
      return;
    }

    const url = this.urlControl?.value?.trim();
    if (!url) return;

    this.loading = true;
    this.error = null;
    this.analysisResult = null;

    this.http.post<AnalysisResult>(`${environment.apiUrl}/api/url/analyze`, { url })
      .pipe(
        takeUntil(this.destroy$),
        finalize(() => this.loading = false)
      )
      .subscribe({
        next: (response) => {
          this.analysisResult = response;
          this.updateChartData(response);
          this.saveLogEntry(url, response);
          this.showSuccessMessage();
        },
        error: (error: HttpErrorResponse) => {
          this.handleError(error);
        }
      });
  }

  private updateChartData(result: AnalysisResult): void {
    this.chartData = [
      { name: 'Autoencoder Score', value: Number(result.autoencoder_score.toFixed(4)) },
      { name: 'XGBoost Score', value: Number(result.xgboost_score.toFixed(4)) }
    ];
  }

  private saveLogEntry(url: string, result: AnalysisResult): void {
    const logEntry = {
      input_type: 'URL',
      input_data: url,
      classification_result: result.is_phishing ? 'Phishing' : 'Safe',
      created_at: new Date()
    };

    this.phishingLogService.saveLog(logEntry)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => console.log('Log entry saved successfully'),
        error: (error) => console.error('Failed to save log entry:', error)
      });
  }

  private handleError(error: HttpErrorResponse): void {
    let errorMessage = 'An unexpected error occurred. Please try again.';
    
    if (error.error?.message) {
      errorMessage = error.error.message;
    } else if (error.status === 0) {
      errorMessage = 'Unable to connect to the server. Please check your internet connection.';
    } else if (error.status >= 400 && error.status < 500) {
      errorMessage = 'Invalid request. Please check the URL format.';
    } else if (error.status >= 500) {
      errorMessage = 'Server error. Please try again later.';
    }

    this.error = errorMessage;
    this.snackBar.open(errorMessage, 'Close', {
      duration: 5000,
      panelClass: ['error-snackbar']
    });
  }

  private showSuccessMessage(): void {
    const message = this.analysisResult?.is_phishing 
      ? 'Analysis complete: Phishing detected!' 
      : 'Analysis complete: URL appears safe.';
    
    this.snackBar.open(message, 'Close', {
      duration: 3000,
      panelClass: this.analysisResult?.is_phishing ? ['warning-snackbar'] : ['success-snackbar']
    });
  }

  onReset(): void {
    this.urlForm.reset();
    this.analysisResult = null;
    this.chartData = [];
    this.error = null;
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}