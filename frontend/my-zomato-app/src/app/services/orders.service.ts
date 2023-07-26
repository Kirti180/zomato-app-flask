import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class OrdersService {
  private apiUrl = 'https://zomato-dugp.onrender.com/orders'; // Update with your API URL

  constructor(private http: HttpClient) { }

  getOrders(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  createOrder(order: any): Observable<any> {
    return this.http.post(this.apiUrl, order);
  }
}
