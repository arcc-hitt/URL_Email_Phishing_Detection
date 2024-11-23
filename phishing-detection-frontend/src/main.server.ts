import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { config } from './app/app.config.server';
import { importProvidersFrom } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

const bootstrap = () => bootstrapApplication(AppComponent, {
  ...config,
  providers: [
    ...(config.providers || []),
    importProvidersFrom(HttpClientModule)  // Import HttpClientModule here
  ]
});

export default bootstrap;
