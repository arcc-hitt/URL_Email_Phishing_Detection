import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

// Bootstrap the application with error handling
bootstrapApplication(AppComponent, appConfig)
  .catch(err => {
    console.error('Application bootstrap failed:', err);
    
    // Show user-friendly error message
    const errorDiv = document.createElement('div');
    errorDiv.innerHTML = `
      <div style="
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #fff;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        text-align: center;
        font-family: 'Roboto', sans-serif;
        max-width: 400px;
      ">
        <h2 style="color: #d32f2f; margin-bottom: 1rem;">
          ⚠️ Application Error
        </h2>
        <p style="color: #666; margin-bottom: 1.5rem;">
          The application failed to load. Please try refreshing the page.
        </p>
        <button 
          onclick="window.location.reload()" 
          style="
            background: #1976d2;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.875rem;
          "
        >
          Refresh Page
        </button>
      </div>
    `;
    document.body.appendChild(errorDiv);
  });