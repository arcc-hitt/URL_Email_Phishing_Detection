import { Component, OnInit, OnDestroy, inject, PLATFORM_ID, ChangeDetectionStrategy, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatSelectModule } from '@angular/material/select';
import { MatOptionModule } from '@angular/material/core';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { Subject, takeUntil } from 'rxjs';

import { PhishingLogService } from '../phishing-log/phishing-log.service';
import { environment } from '../../../environments/environment';

interface EmailData {
  id: string;
  sender: string;
  receiver: string;
  date: string;
  subject: string;
  body: string;
  urls: number;
}

interface AnalysisResult {
  autoencoder_score: number;
  lightgbm_score: number;
  is_phishing: boolean;
}

@Component({
  selector: 'app-email-analysis',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatOptionModule,
    MatProgressSpinnerModule,
    ReactiveFormsModule,
    CommonModule,
    NgxChartsModule
  ],
  templateUrl: './email-analysis.component.html',
  styleUrls: ['./email-analysis.component.scss']
})
export class EmailAnalysisComponent implements OnInit, OnDestroy {
  private readonly destroy$ = new Subject<void>();
  private readonly http = inject(HttpClient);
  private readonly fb = inject(FormBuilder);
  private readonly platformId = inject(PLATFORM_ID);
  private readonly phishingLogService = inject(PhishingLogService);

  public readonly emailForm: FormGroup = this.fb.group({
    sender: ['', [Validators.required, Validators.email]],
    receiver: ['', [Validators.required, Validators.email]],
    date: ['', Validators.required],
    subject: ['', [Validators.required, Validators.maxLength(500)]],
    body: ['', [Validators.required, Validators.maxLength(10000)]],
    urls: [0, [Validators.required, Validators.min(0)]]
  });

  public readonly analysisResult = signal<AnalysisResult | null>(null);
  public readonly isAuthenticated = signal(false);
  public readonly emailList = signal<EmailData[]>([]);
  public readonly selectedEmailId = signal<string>('');
  public readonly chartData = signal<Array<{ name: string; value: number }>>([]);
  public readonly view: [number, number] = [700, 400];
  public readonly loading = signal(false);

  public ngOnInit(): void {
    this.analysisResult.set(null);
    if (isPlatformBrowser(this.platformId)) {
      this.initializeGoogleAPI();
    }
  }

  public ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private async initializeGoogleAPI(): Promise<void> {
    try {
      const { gapi, loadGapiInsideDOM } = await import('gapi-script');
      await loadGapiInsideDOM();
      
      gapi.load('client:auth2', async () => {
        await gapi.client.init({
          apiKey: environment.googleClientSecret,
          clientId: environment.googleClientId,
          discoveryDocs: environment.discoveryDocs,
          scope: environment.gmailScope,
        });
        this.isAuthenticated.set(gapi.auth2.getAuthInstance().isSignedIn.get());
      });
    } catch (error) {
      console.error('Failed to initialize Google API:', error);
    }
  }

  public async connectGmail(): Promise<void> {
    this.analysisResult.set(null);
    try {
      const { gapi } = await import('gapi-script');
      await gapi.auth2.getAuthInstance().signIn();
      this.isAuthenticated.set(true);
    } catch (error) {
      console.error('Gmail connection failed:', error);
    }
  }

  public async disconnectGmail(): Promise<void> {
    try {
      const { gapi } = await import('gapi-script');
      await gapi.auth2.getAuthInstance().signOut();
      this.isAuthenticated.set(false);
      this.emailList.set([]);
      this.analysisResult.set(null);
    } catch (error) {
      console.error('Gmail disconnection failed:', error);
    }
  }

  public async fetchAllEmails(): Promise<void> {
    if (!this.isAuthenticated()) return;

    this.loading.set(true);
    try {
      const { gapi } = await import('gapi-script');
      const response = await gapi.client.gmail.users.messages.list({
        userId: 'me',
        maxResults: 10
      });

      const emails = await Promise.all(
        response.result.messages.map(async (msg: any) => {
          const emailData = await gapi.client.gmail.users.messages.get({
            userId: 'me',
            id: msg.id
          });
          const emailDetails = this.extractEmailDetails(emailData.result);
          return { id: msg.id, ...emailDetails };
        })
      );

      this.emailList.set(emails);
      this.analysisResult.set(null);
    } catch (error) {
      console.error('Failed to fetch emails:', error);
    } finally {
      this.loading.set(false);
    }
  }

  public onEmailSelect(): void {
    const selectedId = this.selectedEmailId();
    if (selectedId) {
      const email = this.emailList().find(e => e.id === selectedId);
      if (email) {
        this.analysisResult.set(null);
        this.analyzeEmail(email);
      }
    }
  }

  private extractEmailDetails(email: any): Omit<EmailData, 'id'> {
    const headers = email.payload.headers;
    const sender = headers.find((h: any) => h.name === 'From')?.value || '';
    const receiver = headers.find((h: any) => h.name === 'To')?.value || '';
    const date = headers.find((h: any) => h.name === 'Date')?.value || '';
    const subject = headers.find((h: any) => h.name === 'Subject')?.value || '';

    // Get body content, decoding if necessary
    let body = email.payload.parts?.[0]?.body?.data || '';
    if (body) {
      try {
        body = atob(body.replace(/-/g, '+').replace(/_/g, '/'));
      } catch (error) {
        console.warn('Failed to decode email body:', error);
        body = '';
      }
    }

    // Count URLs in the email body
    const urlRegex = /https?:\/\/[^\s]+/g;
    const foundUrls = body.match(urlRegex);
    const urls = foundUrls ? 1 : 0;

    return { sender, receiver, date, subject, body, urls };
  }

  private analyzeEmail(payload: Partial<EmailData>): void {
    this.loading.set(true);
    
    this.http.post<AnalysisResult>(`${environment.apiUrl}/api/email/analyze`, payload)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          this.analysisResult.set(response);
          this.updateChartData(response);
          this.saveLogEntry(payload, response);
        },
        error: (error) => {
          console.error('Error analyzing email:', error);
          this.analysisResult.set(null);
        },
        complete: () => {
          this.loading.set(false);
        }
      });
  }

  private updateChartData(result: AnalysisResult): void {
    this.chartData.set([
      { name: 'Autoencoder Score', value: Number(result.autoencoder_score.toFixed(4)) },
      { name: 'LightGBM Score', value: Number(result.lightgbm_score.toFixed(4)) }
    ]);
  }

  private saveLogEntry(payload: Partial<EmailData>, result: AnalysisResult): void {
    const logEntry = {
      input_type: 'Email',
      input_data: payload.subject || '',
      classification_result: result.is_phishing ? 'Phishing' : 'Safe',
      created_at: new Date()
    };

    this.phishingLogService.saveLog(logEntry)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => console.log('Log entry saved successfully'),
        error: (error) => console.error('Error saving log entry:', error)
      });
  }

  public onSubmit(): void {
    if (!this.emailForm.valid) {
      this.emailForm.markAllAsTouched();
      return;
    }

    const payload = this.emailForm.value;
    this.analyzeEmail(payload);
    this.analysisResult.set(null);
  }

  public onReset(): void {
    this.emailForm.reset();
    this.analysisResult.set(null);
    this.chartData.set([]);
  }
}