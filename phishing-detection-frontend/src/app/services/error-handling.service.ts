// src/app/services/error-handling.service.ts
import { Injectable } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, throwError } from 'rxjs';

export interface ErrorInfo {
  message: string;
  code?: string;
  details?: any;
}

@Injectable({
  providedIn: 'root'
})
export class ErrorHandlingService {
  constructor(private snackBar: MatSnackBar) {}

  handleError(error: HttpErrorResponse | Error): Observable<never>  {
    let errorInfo: ErrorInfo;

    if (error instanceof HttpErrorResponse) {
      errorInfo = this.handleHttpError(error);
    } else {
      errorInfo = this.handleGenericError(error);
    }

    this.showErrorMessage(errorInfo.message);
    console.error('Application Error:', errorInfo);
    
    return throwError(() => errorInfo);
  }

  private handleHttpError(error: HttpErrorResponse): ErrorInfo {
    let message = 'An unexpected error occurred. Please try again.';
    
    switch (error.status) {
      case 0:
        message = 'Unable to connect to the server. Please check your internet connection.';
        break;
      case 400:
        message = error.error?.message || 'Invalid request. Please check your input.';
        break;
      case 401:
        message = 'You are not authorized to perform this action.';
        break;
      case 403:
        message = 'Access forbidden. You do not have permission to access this resource.';
        break;
      case 404:
        message = 'The requested resource was not found.';
        break;
      case 422:
        message = error.error?.message || 'Validation error. Please check your input.';
        break;
      case 429:
        message = 'Too many requests. Please wait before trying again.';
        break;
      case 500:
        message = 'Internal server error. Please try again later.';
        break;
      case 502:
      case 503:
        message = 'Service temporarily unavailable. Please try again later.';
        break;
      case 504:
        message = 'Request timeout. Please try again.';
        break;
      default:
        message = error.error?.message || `Server error (${error.status}). Please try again.`;
    }

    return {
      message,
      code: error.status.toString(),
      details: error.error
    };
  }

  private handleGenericError(error: Error): ErrorInfo {
    return {
      message: error.message || 'An unexpected error occurred.',
      details: error
    };
  }

  private showErrorMessage(message: string): void {
    this.snackBar.open(message, 'Close', {
      duration: 5000,
      panelClass: ['error-snackbar'],
      horizontalPosition: 'end',
      verticalPosition: 'top'
    });
  }

  showSuccessMessage(message: string): void {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
      panelClass: ['success-snackbar'],
      horizontalPosition: 'end',
      verticalPosition: 'top'
    });
  }

  showWarningMessage(message: string): void {
    this.snackBar.open(message, 'Close', {
      duration: 4000,
      panelClass: ['warning-snackbar'],
      horizontalPosition: 'end',
      verticalPosition: 'top'
    });
  }
}