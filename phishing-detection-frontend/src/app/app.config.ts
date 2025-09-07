import { ApplicationConfig, provideZoneChangeDetection, importProvidersFrom, ErrorHandler } from '@angular/core';
import { provideRouter, withEnabledBlockingInitialNavigation, withInMemoryScrolling } from '@angular/router';
import { HttpClientModule, provideHttpClient, withInterceptors, withFetch } from '@angular/common/http';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

import { routes } from './app.routes';
import { ErrorHandlingService } from './services/error-handling.service';

// Global error handler
export class GlobalErrorHandler implements ErrorHandler {
  constructor(private errorService: ErrorHandlingService) {}

  handleError(error: any): void {
    console.error('Global error caught:', error);
    
    if (error?.rejection) {
      // Handle promise rejections
      this.errorService.handleError(error.rejection);
    } else {
      // Handle other errors
      this.errorService.handleError(error);
    }
  }
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ 
      eventCoalescing: true,
      runCoalescing: true 
    }),
    provideRouter(
      routes,
      withEnabledBlockingInitialNavigation(),
      withInMemoryScrolling({
        scrollPositionRestoration: 'enabled',
        anchorScrolling: 'enabled'
      })
    ),
    provideClientHydration(withEventReplay()),
    provideAnimationsAsync(),
    provideHttpClient(
      withFetch(),
      withInterceptors([])
    ),
    importProvidersFrom(HttpClientModule),
    {
      provide: ErrorHandler,
      useClass: GlobalErrorHandler,
      deps: [ErrorHandlingService]
    }
  ]
};