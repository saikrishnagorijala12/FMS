import { Injectable } from '@angular/core';
import { jwtDecode } from 'jwt-decode';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class TokenVerificationService {

  constructor(private router: Router) {}

  // Get token from localStorage (or sessionStorage)
  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  // Check if token expired
  isTokenExpired(token?: string): boolean {
    if (!token) token = this.getToken() || '';

    if (!token) return true;
    try {
      const decoded: any = jwtDecode(token);
      if (!decoded.exp) return true;

      const expiryTime = decoded.exp * 1000; // exp is in seconds
      return Date.now() > expiryTime;
    } catch (e) {
      console.error('Invalid token', e);
      return true;
    }
  }

  // Redirect to login if expired
  checkTokenAndRedirect(): void {
    const token = this.getToken();
    if (this.isTokenExpired(token || '')) {
      localStorage.removeItem('access_token');
      this.router.navigate(['/login']);
    }
  }
}