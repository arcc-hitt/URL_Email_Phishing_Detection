import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';
import { CommonModule } from '@angular/common';
import { isPlatformBrowser } from '@angular/common';
import { MatOptionModule } from '@angular/material/core';
import { MatSelectModule } from '@angular/material/select';
import { PhishingLogService } from '../phishing-log/phishing-log.service';
import { environment } from '../../../environments/environment';

@Component({
    selector: 'app-email-analysis',
    imports: [
        MatGridListModule,
        MatCardModule,
        MatButtonModule,
        MatIconModule,
        MatFormFieldModule,
        MatInputModule,
        MatOptionModule,
        MatSelectModule,
        RouterModule,
        FormsModule,
        CommonModule,
        HttpClientModule,
        NgxChartsModule
    ],
    templateUrl: './email-analysis.component.html',
    styleUrls: ['./email-analysis.component.scss']
})
export class EmailAnalysisComponent implements OnInit {
  sender: string = '';
  receiver: string = '';
  date: string = '';
  subject: string = '';
  body: string = '';
  urls: number = 0;
  analysisResult: any = null;
  isAuthenticated: boolean = false;
  emailList: any[] = [];
  selectedEmailId: string = '';
  chartData: any[] = [];
  view: [number, number] = [700, 400];

  constructor(private http: HttpClient, @Inject(PLATFORM_ID) private platformId: any, private phishingLogService: PhishingLogService) {}

  async ngOnInit() {
    this.analysisResult = null;
    if (isPlatformBrowser(this.platformId)) {
      const { gapi, loadGapiInsideDOM } = await import('gapi-script');
      await loadGapiInsideDOM();
      
      gapi.load('client:auth2', async () => {
        await gapi.client.init({
          apiKey: environment.googleClientSecret,
          clientId: environment.googleClientId,
          discoveryDocs: environment.discoveryDocs,
          scope: environment.gmailScope,
        });
        this.isAuthenticated = gapi.auth2.getAuthInstance().isSignedIn.get();
      });
    }
  }  
  
  async connectGmail() {
    this.analysisResult = null;
    const { gapi } = await import('gapi-script');
    gapi.auth2.getAuthInstance().signIn().then(() => {
      this.isAuthenticated = true;
    });
  }

  async disconnectGmail() {
    const { gapi } = await import('gapi-script');
    gapi.auth2.getAuthInstance().signOut().then(() => {
      this.isAuthenticated = false;
      this.emailList = [];
      this.analysisResult = null;
    });
  }

  async fetchAllEmails() {
    if (!this.isAuthenticated) return;

    const { gapi } = await import('gapi-script');
    const response = await gapi.client.gmail.users.messages.list({
      userId: 'me',
      maxResults: 10
    });

    this.emailList = await Promise.all(
      response.result.messages.map(async (msg: any) => {
        const emailData = await gapi.client.gmail.users.messages.get({
          userId: 'me',
          id: msg.id
        });
        const emailDetails = this.extractEmailDetails(emailData.result);
        return { id: msg.id, ...emailDetails };
      })
    );

    this.analysisResult = null; // Clear any previous analysis result on fetch
  }

  onEmailSelect() {
    if (this.selectedEmailId) {
      const email = this.emailList.find((e) => e.id === this.selectedEmailId);
      if (email) {
        this.analysisResult = null; // Clear result before new analysis
        this.analyzeEmail(email);
      }
    }
  }

  extractEmailDetails(email: any) {
    const headers = email.payload.headers;
    const sender = headers.find((h: any) => h.name === 'From')?.value || '';
    const receiver = headers.find((h: any) => h.name === 'To')?.value || '';
    const date = headers.find((h: any) => h.name === 'Date')?.value || '';
    const subject = headers.find((h: any) => h.name === 'Subject')?.value || '';
  
    // Get body content, decoding if necessary (assume base64 encoding if encoded)
    let body = email.payload.parts?.[0]?.body?.data || '';
    body = body ? atob(body.replace(/-/g, '+').replace(/_/g, '/')) : '';
  
    // Regular expression to match URLs in the email body
    const urlRegex = /https?:\/\/[^\s]+/g;
    const foundUrls = body.match(urlRegex);
  
    // Set the 'urls' value: 1 if at least one URL is found, otherwise 0
    const urls = foundUrls ? 1 : 0;
  
    return { sender, receiver, date, subject, body, urls };
  }  

  analyzeEmail(payload: any) {
    this.http.post<any>(`${environment.apiUrl}/api/email/analyze`, payload).subscribe({
      next: (response) => {
        this.analysisResult = response;
        this.updateChartData();

        // Prepare log entry data
        const logEntry = {
          input_type: 'Email',
          input_data: payload.subject,
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
        console.error('Error analyzing email:', error);
        this.analysisResult = { error: 'Error analyzing email.' };
      }
    });
  }

  updateChartData() {
    if (this.analysisResult) {
      this.chartData = [
        { name: 'Autoencoder Score', value: this.analysisResult.autoencoder_score },
        { name: 'LightGBM Score', value: this.analysisResult.lightgbm_score },
      ];
    }
  }
  
  onSubmit() {
    const payload = {
      sender: this.sender,
      receiver: this.receiver,
      date: this.date,
      subject: this.subject,
      body: this.body,
      urls: this.urls
    };

    this.analyzeEmail(payload);
    this.analysisResult = null;
  }
}