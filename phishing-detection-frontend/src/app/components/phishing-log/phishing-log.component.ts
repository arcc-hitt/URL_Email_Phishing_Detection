import { Component, OnInit, OnDestroy, inject, ChangeDetectionStrategy, signal, TrackByFunction } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ReactiveFormsModule, FormControl } from '@angular/forms';
import { CommonModule, DatePipe } from '@angular/common';
import { Subject, takeUntil, debounceTime, distinctUntilChanged } from 'rxjs';

import { environment } from '../../../environments/environment';

interface LogEntry {
  _id?: string;
  input_type: string;
  input_data: string;
  classification_result: string;
  created_at: Date | string;
}

@Component({
  selector: 'app-phishing-log',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [
    MatTableModule,
    MatCardModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    ReactiveFormsModule,
    CommonModule
  ],
  templateUrl: './phishing-log.component.html',
  styleUrls: ['./phishing-log.component.scss'],
  providers: [DatePipe]
})
export class PhishingLogComponent implements OnInit, OnDestroy {
  private readonly destroy$ = new Subject<void>();
  private readonly http = inject(HttpClient);

  public readonly searchControl = new FormControl('');
  public readonly logs = signal<LogEntry[]>([]);
  public readonly filteredLogs = signal<LogEntry[]>([]);
  public readonly displayedLogs = signal<LogEntry[]>([]);
  public readonly loading = signal(false);
  public readonly error = signal<string | null>(null);

  public readonly displayedColumns: readonly string[] = [
    'input_type', 
    'input_data', 
    'classification_result', 
    'created_at'
  ] as const;

  // Pagination
  public readonly currentPage = signal(1);
  public readonly totalPages = signal(1);
  public readonly itemsPerPage = 10;

  // TrackBy function for mat-table
  public readonly trackByLogId: TrackByFunction<LogEntry> = (index: number, log: LogEntry): string => {
    return log._id || `${log.input_type}-${log.created_at}-${index}`;
  };

  public ngOnInit(): void {
    this.loadLogs();
    this.setupSearch();
  }

  public ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private setupSearch(): void {
    this.searchControl.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      takeUntil(this.destroy$)
    ).subscribe(() => {
      this.applyFilter();
    });
  }

  private loadLogs(): void {
    this.loading.set(true);
    this.error.set(null);

    this.http.get<LogEntry[]>(`${environment.apiUrl}/api/phishing_logs`)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data: LogEntry[]) => {
          // Sort by created_at in descending order (newest first)
          const sortedData = data.sort((a, b) => {
            const dateA = new Date(a.created_at).getTime();
            const dateB = new Date(b.created_at).getTime();
            return dateB - dateA;
          });
          
          this.logs.set(sortedData);
          this.applyFilter();
          this.loading.set(false);
        },
        error: (err: HttpErrorResponse) => {
          this.handleError(err);
          this.loading.set(false);
        }
      });
  }

  private handleError(error: HttpErrorResponse): void {
    let errorMessage = 'An error occurred while loading logs.';
    
    if (error.status === 0) {
      errorMessage = 'Unable to connect to the server. Please check your connection.';
    } else if (error.status >= 400 && error.status < 500) {
      errorMessage = 'Invalid request. Please try again.';
    } else if (error.status >= 500) {
      errorMessage = 'Server error. Please try again later.';
    }
    
    this.error.set(errorMessage);
    console.error('Error loading logs:', error);
  }

  public applyFilter(): void {
    const searchTerm = this.searchControl.value?.toLowerCase() || '';
    const allLogs = this.logs();
    
    let filtered: LogEntry[];
    if (!searchTerm.trim()) {
      filtered = [...allLogs];
    } else {
      filtered = allLogs.filter(log => 
        log.input_type.toLowerCase().includes(searchTerm) ||
        log.input_data.toLowerCase().includes(searchTerm) ||
        log.classification_result.toLowerCase().includes(searchTerm) ||
        new Date(log.created_at).toLocaleDateString().toLowerCase().includes(searchTerm)
      );
    }

    this.filteredLogs.set(filtered);
    this.calculatePagination();
    this.currentPage.set(1); // Reset to first page
    this.updateDisplayedLogs();
  }

  private calculatePagination(): void {
    const totalItems = this.filteredLogs().length;
    const pages = Math.ceil(totalItems / this.itemsPerPage);
    this.totalPages.set(Math.max(1, pages));
  }

  private updateDisplayedLogs(): void {
    const filtered = this.filteredLogs();
    const start = (this.currentPage() - 1) * this.itemsPerPage;
    const end = start + this.itemsPerPage;
    this.displayedLogs.set(filtered.slice(start, end));
  }

  public nextPage(): void {
    const current = this.currentPage();
    const total = this.totalPages();
    if (current < total) {
      this.currentPage.set(current + 1);
      this.updateDisplayedLogs();
    }
  }

  public previousPage(): void {
    const current = this.currentPage();
    if (current > 1) {
      this.currentPage.set(current - 1);
      this.updateDisplayedLogs();
    }
  }

  public refreshLogs(): void {
    this.loadLogs();
  }

  public clearSearch(): void {
    this.searchControl.setValue('');
  }

  public getResultClass(result: string): string {
    return result.toLowerCase() === 'phishing' ? 'phishing-result' : 'safe-result';
  }

  public getTypeIcon(type: string): string {
    switch (type.toLowerCase()) {
      case 'url':
        return 'link';
      case 'email':
        return 'email';
      default:
        return 'description';
    }
  }

  public formatDate(date: Date | string): string {
    try {
      return new Date(date).toLocaleString();
    } catch {
      return 'Invalid Date';
    }
  }
}