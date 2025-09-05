// src/app/services/security.service.ts
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SecurityService {

  /**
   * Validates URL format and security
   */
  validateUrl(url: string): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];
    
    if (!url || url.trim().length === 0) {
      errors.push('URL is required');
      return { isValid: false, errors };
    }

    const trimmedUrl = url.trim();

    // Check if URL starts with http or https
    if (!trimmedUrl.match(/^https?:\/\//)) {
      errors.push('URL must start with http:// or https://');
    }

    // Check for valid URL format
    try {
      const urlObj = new URL(trimmedUrl);
      
      // Check for suspicious patterns
      if (this.containsSuspiciousPatterns(trimmedUrl)) {
        errors.push('URL contains suspicious patterns');
      }

      // Validate domain
      if (!this.isValidDomain(urlObj.hostname)) {
        errors.push('Invalid domain format');
      }

    } catch (e) {
      errors.push('Invalid URL format');
    }

    return { isValid: errors.length === 0, errors };
  }

  /**
   * Sanitizes user input to prevent XSS
   */
  sanitizeInput(input: string): string {
    if (!input) return '';
    
    return input
      .replace(/[<>]/g, '') // Remove basic HTML tags
      .replace(/javascript:/gi, '') // Remove javascript: protocol
      .replace(/on\w+=/gi, '') // Remove event handlers
      .trim();
  }

  /**
   * Validates email content for analysis
   */
  validateEmailContent(email: {
    sender?: string;
    receiver?: string;
    subject?: string;
    body?: string;
  }): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (email.sender && !this.isValidEmail(email.sender)) {
      errors.push('Invalid sender email format');
    }

    if (email.receiver && !this.isValidEmail(email.receiver)) {
      errors.push('Invalid receiver email format');
    }

    if (!email.subject || email.subject.trim().length === 0) {
      errors.push('Email subject is required');
    }

    if (!email.body || email.body.trim().length === 0) {
      errors.push('Email body is required');
    }

    // Check for content length limits
    if (email.subject && email.subject.length > 500) {
      errors.push('Email subject is too long (max 500 characters)');
    }

    if (email.body && email.body.length > 10000) {
      errors.push('Email body is too long (max 10,000 characters)');
    }

    return { isValid: errors.length === 0, errors };
  }

  private containsSuspiciousPatterns(url: string): boolean {
    const suspiciousPatterns = [
      /javascript:/i,
      /data:/i,
      /vbscript:/i,
      /<script/i,
      /onload=/i,
      /onerror=/i,
    ];

    return suspiciousPatterns.some(pattern => pattern.test(url));
  }

  private isValidDomain(domain: string): boolean {
    const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9](?:\.[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9])*$/;
    return domainRegex.test(domain);
  }

  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  /**
   * Rate limiting check (simple client-side implementation)
   */
  checkRateLimit(key: string, maxRequests: number = 10, windowMs: number = 60000): boolean {
    const now = Date.now();
    const windowKey = `rate_limit_${key}`;
    
    let requests = JSON.parse(localStorage.getItem(windowKey) || '[]');
    
    // Clean old requests
    requests = requests.filter((timestamp: number) => now - timestamp < windowMs);
    
    if (requests.length >= maxRequests) {
      return false; // Rate limit exceeded
    }
    
    requests.push(now);
    localStorage.setItem(windowKey, JSON.stringify(requests));
    
    return true;
  }

  /**
   * Content Security Policy helpers
   */
  generateCSPNonce(): string {
    const array = new Uint8Array(16);
    crypto.getRandomValues(array);
    return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
  }
}