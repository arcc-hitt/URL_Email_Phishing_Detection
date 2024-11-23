import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { PhishingLogComponent } from './components/phishing-log/phishing-log.component';
import { EmailAnalysisComponent } from './components/email-analysis/email-analysis.component';
import { UrlAnalysisComponent } from './components/url-analysis/url-analysis.component';

export const routes: Routes = [
  { path: 'dashboard', component: DashboardComponent },
  { path: 'phishing-log', component: PhishingLogComponent },
  { path: 'email-analysis', component: EmailAnalysisComponent },
  { path: 'url-analysis', component: UrlAnalysisComponent },
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' } // Default route
];

