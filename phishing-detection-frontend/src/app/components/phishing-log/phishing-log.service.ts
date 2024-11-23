import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class PhishingLogService {
  constructor(private http: HttpClient) {}

  // Add a method to save log entries to the database
  saveLog(entry: any) {
    return this.http.post<any>('http://localhost:5000/api/phishing_logs', entry);
  }
}