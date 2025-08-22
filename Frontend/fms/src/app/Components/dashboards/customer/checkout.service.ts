// checkout.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class CheckoutService {
  private apiUrl = 'http://localhost:5000/orders'; 

  constructor(private http: HttpClient) {}

  checkout(payload: any, token: string): Observable<any> {
  const headers = new HttpHeaders({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}` 
  });
  return this.http.post(this.apiUrl, payload, { headers });
}
}
