import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class PhishingLogService {
  constructor(private http: HttpClient) {}

  // Add a method to save log entries to the database
  saveLog(entry: any) {
    return this.http.post<any>(`${environment.apiUrl}/api/phishing_logs`, entry);
  }
}