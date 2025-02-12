import { Component, OnInit } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon'; // Import MatIconModule
import { MatFormFieldModule } from '@angular/material/form-field'; // Import MatFormFieldModule
import { MatInputModule } from '@angular/material/input'; // Import MatInputModule
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { MatButtonModule } from '@angular/material/button';
import { MatGridListModule } from '@angular/material/grid-list';
import { DatePipe } from '@angular/common';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule, HttpErrorResponse } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Component({
    selector: 'app-phishing-log',
    imports: [
        MatGridListModule,
        MatCardModule,
        CommonModule,
        MatButtonModule,
        MatIconModule, // Add MatIconModule here
        MatFormFieldModule, // Add MatFormFieldModule here
        MatInputModule, // Add MatInputModule here
        RouterModule,
        FormsModule,
        MatTableModule,
        MatCardModule,
        HttpClientModule,
    ], templateUrl: './phishing-log.component.html',
    styleUrls: ['./phishing-log.component.scss'],
    providers: [DatePipe] // Add DatePipe to providers
})
export class PhishingLogComponent implements OnInit {
  logs: any[] = [];
  displayedLogs: any[] = []; // Holds the logs for the current page
  filteredLogs: any[] = [];
  displayedColumns: string[] = ['input_type', 'input_data', 'classification_result', 'created_at'];
  currentPage: number = 1;
  totalPages: number = 1;
  itemsPerPage: number = 10;
  searchTerm: string = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadLogs();
  }

  loadLogs() {
    this.http.get<any[]>(`${environment.apiUrl}/api/phishing_logs`).subscribe({
      next: (data) => {
        this.logs = data;
        this.applyFilter(); // Initially apply the filter to display the first page
      },
      error: (err: HttpErrorResponse) => {
        console.error('Error loading logs:', err.message);
      },
    });
  }

  // Calculates logs for the current page
  updateDisplayedLogs() {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    const end = start + this.itemsPerPage;
    this.displayedLogs = this.filteredLogs.slice(start, end);
  }

  nextPage() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.updateDisplayedLogs();
    }
  }

  previousPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.updateDisplayedLogs();
    }
  }

  // Filters logs and updates pagination
  applyFilter() {
    this.filteredLogs = this.logs.filter((log) =>
      Object.values(log)
        .join(' ')
        .toLowerCase()
        .includes(this.searchTerm.toLowerCase())
    );
    this.totalPages = Math.ceil(this.filteredLogs.length / this.itemsPerPage);
    this.currentPage = 1; // Reset to first page after filtering
    this.updateDisplayedLogs();
  }
}