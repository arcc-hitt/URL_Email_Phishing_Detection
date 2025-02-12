import { Component } from '@angular/core';
import { HttpClientModule, HttpClient } from '@angular/common/http';  // Import HttpClientModule and HttpClient
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon'; // Import MatIconModule
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { PhishingLogService } from '../phishing-log/phishing-log.service';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { environment } from '../../../environments/environment';

@Component({
    selector: 'app-url-analysis',
    standalone: true,
    imports: [
        MatCardModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        CommonModule,
        MatIconModule,
        RouterModule,
        FormsModule,
        MatProgressSpinnerModule,
        ReactiveFormsModule,
        HttpClientModule,
        NgxChartsModule
    ],
    templateUrl: './url-analysis.component.html',
    styleUrls: ['./url-analysis.component.scss']
})
export class UrlAnalysisComponent {
  urlForm: FormGroup;
  result: string | null = null;
  loading = false;
  chartData: any = null;
  view: [number, number] = [700, 400];
  analysisResult: any;

  constructor(private fb: FormBuilder, private http: HttpClient, private phishingLogService: PhishingLogService) {
    this.urlForm = this.fb.group({
      url: ['', [Validators.required, Validators.pattern('https?://.+')]],
    });
  }

  onSubmit() {
    if (this.urlForm.valid) {
      const url = this.urlForm.get('url')?.value;

      this.http.post<any>(`${environment.apiUrl}/api/url/analyze`, { url }).subscribe({
        next: (response) => {
          this.analysisResult = response;
          this.loading = false;

          // Prepare data for the chart
          this.chartData = [
            { name: 'Autoencoder Score', value: response.autoencoder_score },
            { name: 'XGBoost Score', value: response.xgboost_score }
          ];

          // Prepare log entry data
          const logEntry = {
            input_type: 'URL',
            input_data: url,
            classification_result: response.is_phishing ? 'Phishing' : 'Safe',
            created_at: new Date()
          };

          // Save log entry to MongoDB
          this.phishingLogService.saveLog(logEntry).subscribe(
            (res) => console.log('Log entry saved:', res),
            (error) => console.error('Error saving log entry:', error)
          );
        },
        error: (error) => {
          this.loading = false;
          console.error('Error analyzing URL:', error);
        }
      });
    }
  }
}

